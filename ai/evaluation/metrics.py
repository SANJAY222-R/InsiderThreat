import torch
import torchmetrics
from typing import Dict

class ModelEvaluator:
    """
    Validation pipeline utilizing torchmetrics.
    Tracks Loss, Accuracy, Precision, Recall, F1, ROC-AUC.
    """
    def __init__(self, device: torch.device):
        self.device = device
        
        # We assume binary classification for threat detection
        self.metrics = torchmetrics.MetricCollection({
            'accuracy': torchmetrics.Accuracy(task='binary'),
            'precision': torchmetrics.Precision(task='binary'),
            'recall': torchmetrics.Recall(task='binary'),
            'f1': torchmetrics.F1Score(task='binary'),
            'auroc': torchmetrics.AUROC(task='binary')
        }).to(self.device)
        
        self.conf_mat = torchmetrics.ConfusionMatrix(task='binary', num_classes=2).to(self.device)
        
    def update(self, preds: torch.Tensor, targets: torch.Tensor):
        # preds can be logits or probs, torchmetrics handles appropriately based on the metric
        # Ensure they are squeezed and floats/longs properly
        preds = preds.squeeze().float()
        targets = targets.squeeze().long()
        
        self.metrics.update(preds, targets)
        
        # Confusion matrix typically wants discrete predictions if logits are passed, 
        # but binary task AUROC wants continuous.
        # We pass probs to confusion matrix, it will threshold at 0.5 by default.
        probs = torch.sigmoid(preds) if not torch.all((preds >= 0) & (preds <= 1)) else preds
        self.conf_mat.update(probs, targets)
        
    def compute(self) -> Dict[str, float]:
        res = self.metrics.compute()
        res_dict = {k: v.item() for k, v in res.items()}
        return res_dict
        
    def get_confusion_matrix(self) -> torch.Tensor:
        return self.conf_mat.compute()
        
    def reset(self):
        self.metrics.reset()
        self.conf_mat.reset()
