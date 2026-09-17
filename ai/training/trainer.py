import os
import logging
from typing import Any, Dict, List, Optional, Tuple

import torch
import torch.nn as nn

try:
    from tqdm import tqdm  # type: ignore
except (ImportError, ModuleNotFoundError):
    def tqdm(iterable: Any, *args: Any, **kwargs: Any) -> Any:  # type: ignore
        return iterable

try:
    from torch.utils.tensorboard import SummaryWriter  # type: ignore
except (ImportError, ModuleNotFoundError):
    SummaryWriter = None

from ai.evaluation.metrics import ModelEvaluator
from ai.models.loss_functions import THGNNLoss

logger = logging.getLogger(__name__)


class THGNNTrainer:
    """
    Training pipeline for THGNN.
    Supports Mixed Precision (CUDA), TensorBoard (optional), Early Stopping, Gradient Clipping.
    """
    def __init__(self, model: nn.Module, config: Dict[str, Any], device: torch.device, log_dir: str = 'logs') -> None:
        self.model = model.to(device)
        self.config = config
        self.device = device

        self.writer: Any = None
        if SummaryWriter is not None and log_dir:
            try:
                self.writer = SummaryWriter(log_dir)
            except Exception:
                self.writer = None
        
        self.optimizer = torch.optim.AdamW(
            self.model.parameters(), 
            lr=float(config.get('learning_rate', 0.001)), 
            weight_decay=float(config.get('weight_decay', 0.0001))
        )
        
        self.criterion = THGNNLoss(
            loss_type=str(config.get('loss_function', 'focal')),
            class_weights=config.get('class_weights', {'normal': 1.0, 'threat': 1.0})
        ).to(device)
        
        self.is_cuda = self.device.type == 'cuda'
        self.use_amp = bool(config.get('mixed_precision', True) and self.is_cuda)
        if hasattr(torch, 'amp') and hasattr(torch.amp, 'GradScaler'):
            self.scaler: Any = torch.amp.GradScaler('cuda', enabled=self.use_amp)
        else:
            self.scaler = torch.cuda.amp.GradScaler(enabled=self.use_amp)
        self.evaluator = ModelEvaluator(device)
        
        self.target_node = 'user'
        
    def train_epoch(self, dataloader: Any) -> float:
        self.model.train()
        total_loss = 0.0
        
        for batch in tqdm(dataloader, desc="Training"):
            batch = batch.to(self.device)
            self.optimizer.zero_grad()
            
            if self.use_amp:
                with torch.cuda.amp.autocast(enabled=True):
                    preds = self.model(batch)
                    targets = getattr(batch[self.target_node], 'y', None)
                    if targets is None:
                        targets = torch.zeros(batch[self.target_node].x.size(0), device=self.device)
                    loss = self.criterion(preds['node_scores'][self.target_node], targets)

                self.scaler.scale(loss).backward()
                if self.config.get('gradient_clipping', 1.0) > 0:
                    self.scaler.unscale_(self.optimizer)
                    torch.nn.utils.clip_grad_norm_(self.model.parameters(), float(self.config['gradient_clipping']))
                self.scaler.step(self.optimizer)
                self.scaler.update()
            else:
                preds = self.model(batch)
                targets = getattr(batch[self.target_node], 'y', None)
                if targets is None:
                    targets = torch.zeros(batch[self.target_node].x.size(0), device=self.device)
                loss = self.criterion(preds['node_scores'][self.target_node], targets)
                loss.backward()
                if self.config.get('gradient_clipping', 1.0) > 0:
                    torch.nn.utils.clip_grad_norm_(self.model.parameters(), float(self.config['gradient_clipping']))
                self.optimizer.step()
                
            total_loss += float(loss.item())
            
        return total_loss / max(len(dataloader), 1)
        
    def validate(self, dataloader: Any) -> Dict[str, Any]:
        self.model.eval()
        self.evaluator.reset()
        total_loss = 0.0
        
        with torch.no_grad():
            for batch in tqdm(dataloader, desc="Validating"):
                batch = batch.to(self.device)
                
                if self.use_amp:
                    with torch.cuda.amp.autocast(enabled=True):
                        preds = self.model(batch)
                        targets = getattr(batch[self.target_node], 'y', None)
                        if targets is None:
                            targets = torch.zeros(batch[self.target_node].x.size(0), device=self.device)
                        loss = self.criterion(preds['node_scores'][self.target_node], targets)
                else:
                    preds = self.model(batch)
                    targets = getattr(batch[self.target_node], 'y', None)
                    if targets is None:
                        targets = torch.zeros(batch[self.target_node].x.size(0), device=self.device)
                    loss = self.criterion(preds['node_scores'][self.target_node], targets)
                    
                total_loss += float(loss.item())
                self.evaluator.update(preds['node_scores'][self.target_node], targets)
                
        metrics = self.evaluator.compute()
        metrics['val_loss'] = total_loss / max(len(dataloader), 1)
        return metrics
        
    def fit(self, train_loader: Any, val_loader: Any) -> None:
        epochs = int(self.config.get('epochs', 5))
        best_val_auc = -1.0
        patience = int(self.config.get('early_stopping', {}).get('patience', 10))
        patience_counter = 0
        
        for epoch in range(epochs):
            train_loss = self.train_epoch(train_loader)
            val_metrics = self.validate(val_loader)
            val_auc = float(val_metrics.get('auroc', 0.0))
            
            print(f"Epoch {epoch + 1}/{epochs} | Train Loss: {train_loss:.4f} | Val Loss: {val_metrics['val_loss']:.4f} | Val AUC: {val_auc:.4f}")
            logger.info(f"Epoch {epoch}: Train Loss={train_loss:.4f}, Val Loss={val_metrics['val_loss']:.4f}, Val AUC={val_auc:.4f}")
            
            if self.writer is not None:
                self.writer.add_scalar('Loss/train', train_loss, epoch)
                self.writer.add_scalar('Loss/val', val_metrics['val_loss'], epoch)
                self.writer.add_scalar('AUC/val', val_auc, epoch)
            
            if val_auc >= best_val_auc:
                best_val_auc = val_auc
                patience_counter = 0
                self.save_checkpoint(os.path.join('ai', 'checkpoints', 'best_model.pt'))
            else:
                patience_counter += 1
                
            if patience_counter >= patience:
                print(f"Early stopping triggered at epoch {epoch + 1}")
                logger.info(f"Early stopping triggered at epoch {epoch}")
                break
                
        if self.writer is not None:
            self.writer.close()

    def save_checkpoint(self, path: str) -> None:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        torch.save({
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'config': self.config,
        }, path)


def train_thgnn(config_path: str = "configs/model.yaml") -> str:
    """
    Initializes THGNN, loads dataset, trains, and saves checkpoint to ai/checkpoints/best_model.pt.
    """
    import yaml
    from ai.models.thgnn import THGNN
    from ai.data.dataset_loader import GraphDatasetLoader

    logging.basicConfig(level=logging.INFO)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"\n=======================================================")
    print(f"  Building & Training THGNN Model (Device: {device})")
    print(f"=======================================================\n")

    full_config: Dict[str, Any] = {}
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            full_config = yaml.safe_load(f) or {}

    model_config: Dict[str, Any] = full_config.get("model", {}).get("architecture", {
        "hidden_dim": 128,
        "num_layers": 3,
        "num_heads": 8,
        "dropout": 0.2,
        "pooling_type": "attention",
        "time_encoding": "sinusoidal",
    })
    node_types: List[str] = full_config.get("model", {}).get("node_types", [
        "user", "host", "file", "usb", "email", "website", "session", "department"
    ])
    raw_edges: List[List[str]] = full_config.get("model", {}).get("edge_types", [
        ["user", "LOGIN_TO", "host"],
        ["user", "ACCESS_FILE", "file"],
        ["user", "INSERT_USB", "usb"],
        ["user", "SEND_EMAIL", "email"],
        ["user", "VISIT_WEBSITE", "website"],
        ["host", "CONNECT_HOST", "host"],
        ["user", "SESSION_MEMBER", "session"],
        ["user", "BELONGS_TO", "department"],
    ])
    edge_types: List[Tuple[str, str, str]] = [
        (e[0], e[1], e[2]) for e in raw_edges if len(e) >= 3
    ]

    print(f"-> Initializing model architecture ({len(node_types)} node types, {len(edge_types)} edge types)...")
    model = THGNN(
        node_types=node_types,
        edge_types=edge_types,
        hidden_dim=int(model_config.get("hidden_dim", 128)),
        num_layers=int(model_config.get("num_layers", 3)),
        num_heads=int(model_config.get("num_heads", 8)),
        dropout=float(model_config.get("dropout", 0.2)),
        pooling_type=str(model_config.get("pooling_type", "attention")),
        time_encoding=str(model_config.get("time_encoding", "sinusoidal")),
    )

    print("-> Loading / preparing graph dataset...")
    raw_dir = os.path.join("dataset", "graphs")
    os.makedirs(raw_dir, exist_ok=True)
    loader = GraphDatasetLoader(root=raw_dir, filename="graph.pt")
    data = loader.data

    train_loader = [data]
    val_loader = [data]

    training_config: Dict[str, Any] = full_config.get("training", {})
    epochs = min(int(training_config.get("epochs", 5)), 5)
    training_config["epochs"] = epochs

    trainer = THGNNTrainer(
        model=model,
        config=training_config,
        device=device,
        log_dir="logs",
    )

    print(f"-> Training for {epochs} epochs...")
    trainer.fit(train_loader, val_loader)

    checkpoint_path = os.path.join("ai", "checkpoints", "best_model.pt")
    trainer.save_checkpoint(checkpoint_path)

    print(f"\n[SUCCESS] Model built successfully!")
    print(f"[SUCCESS] Checkpoint saved to: {checkpoint_path} ({os.path.getsize(checkpoint_path)} bytes)\n")
    return checkpoint_path


if __name__ == "__main__":
    train_thgnn()
