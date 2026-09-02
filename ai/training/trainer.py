import os
import torch
import torch.nn as nn
from torch.utils.tensorboard import SummaryWriter
import logging
from tqdm import tqdm

from ai.evaluation.metrics import ModelEvaluator
from ai.models.loss_functions import THGNNLoss

logger = logging.getLogger(__name__)

class THGNNTrainer:
    """
    Training pipeline for THGNN.
    Supports Mixed Precision, TensorBoard, Early Stopping, Gradient Clipping.
    """
    def __init__(self, model: nn.Module, config: dict, device: torch.device, log_dir: str = 'logs'):
        self.model = model.to(device)
        self.config = config
        self.device = device
        self.writer = SummaryWriter(log_dir)
        
        self.optimizer = torch.optim.AdamW(
            self.model.parameters(), 
            lr=config.get('learning_rate', 0.001), 
            weight_decay=config.get('weight_decay', 0.0001)
        )
        
        self.criterion = THGNNLoss(
            loss_type=config.get('loss_function', 'focal'),
            class_weights=config.get('class_weights', {'normal': 1.0, 'threat': 1.0})
        ).to(device)
        
        self.scaler = torch.cuda.amp.GradScaler(enabled=config.get('mixed_precision', True))
        self.evaluator = ModelEvaluator(device)
        
        # Assuming target node type for prediction is 'user' for simplicity
        self.target_node = 'user'
        
    def train_epoch(self, dataloader) -> float:
        self.model.train()
        total_loss = 0
        
        for batch in tqdm(dataloader, desc="Training"):
            batch = batch.to(self.device)
            self.optimizer.zero_grad()
            
            # Using autocast for mixed precision
            with torch.cuda.amp.autocast(enabled=self.config.get('mixed_precision', True)):
                preds = self.model(batch)
                
                # Retrieve targets (Assuming they are stored as batch[self.target_node].y)
                targets = getattr(batch[self.target_node], 'y', None)
                if targets is None:
                    # Dummy targets for stubbing
                    targets = torch.zeros(batch[self.target_node].x.size(0), device=self.device)
                
                loss = self.criterion(preds['node_scores'][self.target_node], targets)
                
            self.scaler.scale(loss).backward()
            
            if self.config.get('gradient_clipping', 1.0) > 0:
                self.scaler.unscale_(self.optimizer)
                torch.nn.utils.clip_grad_norm_(self.model.parameters(), self.config['gradient_clipping'])
                
            self.scaler.step(self.optimizer)
            self.scaler.update()
            
            total_loss += loss.item()
            
        return total_loss / len(dataloader)
        
    def validate(self, dataloader) -> dict:
        self.model.eval()
        self.evaluator.reset()
        total_loss = 0
        
        with torch.no_grad():
            for batch in tqdm(dataloader, desc="Validating"):
                batch = batch.to(self.device)
                
                with torch.cuda.amp.autocast(enabled=self.config.get('mixed_precision', True)):
                    preds = self.model(batch)
                    targets = getattr(batch[self.target_node], 'y', None)
                    if targets is None:
                        targets = torch.zeros(batch[self.target_node].x.size(0), device=self.device)
                        
                    loss = self.criterion(preds['node_scores'][self.target_node], targets)
                    
                total_loss += loss.item()
                self.evaluator.update(preds['node_scores'][self.target_node], targets)
                
        metrics = self.evaluator.compute()
        metrics['val_loss'] = total_loss / len(dataloader)
        return metrics
        
    def fit(self, train_loader, val_loader):
        epochs = self.config.get('epochs', 10)
        best_val_auc = 0.0
        patience = self.config.get('early_stopping', {}).get('patience', 10)
        patience_counter = 0
        
        for epoch in range(epochs):
            train_loss = self.train_epoch(train_loader)
            val_metrics = self.validate(val_loader)
            
            logger.info(f"Epoch {epoch}: Train Loss={train_loss:.4f}, Val Loss={val_metrics['val_loss']:.4f}, Val AUC={val_metrics.get('auroc', 0):.4f}")
            
            self.writer.add_scalar('Loss/train', train_loss, epoch)
            self.writer.add_scalar('Loss/val', val_metrics['val_loss'], epoch)
            self.writer.add_scalar('AUC/val', val_metrics.get('auroc', 0), epoch)
            
            if val_metrics.get('auroc', 0) > best_val_auc:
                best_val_auc = val_metrics.get('auroc', 0)
                patience_counter = 0
                self.save_checkpoint(os.path.join('ai/checkpoints', 'best_model.pt'))
            else:
                patience_counter += 1
                
            if patience_counter >= patience:
                logger.info(f"Early stopping triggered at epoch {epoch}")
                break
                
        self.writer.close()

    def save_checkpoint(self, path: str):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        torch.save({
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
        }, path)
