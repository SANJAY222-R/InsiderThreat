import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Dict, Optional

class FocalLoss(nn.Module):
    def __init__(self, alpha: float = 1.0, gamma: float = 2.0, reduction: str = 'mean'):
        super().__init__()
        self.alpha = alpha
        self.gamma = gamma
        self.reduction = reduction

    def forward(self, inputs: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
        bce_loss = F.binary_cross_entropy_with_logits(inputs, targets, reduction='none')
        pt = torch.exp(-bce_loss)
        focal_loss = self.alpha * (1 - pt) ** self.gamma * bce_loss

        if self.reduction == 'mean':
            return focal_loss.mean()
        elif self.reduction == 'sum':
            return focal_loss.sum()
        else:
            return focal_loss

class THGNNLoss(nn.Module):
    """
    Centralized custom losses for THGNN.
    Supports Focal Loss, BCE, CE, and weighted losses for class imbalance.
    """
    def __init__(self, loss_type: str = 'focal', class_weights: Optional[Dict[str, float]] = None):
        super().__init__()
        self.loss_type = loss_type
        self.class_weights = class_weights or {'normal': 1.0, 'threat': 1.0}
        
        # Calculate positive weight based on class weights
        pos_weight = torch.tensor([self.class_weights['threat'] / self.class_weights['normal']])
        
        if self.loss_type == 'focal':
            self.criterion = FocalLoss(alpha=pos_weight.item(), gamma=2.0)
        elif self.loss_type == 'bce':
            self.criterion = nn.BCEWithLogitsLoss(pos_weight=pos_weight)
        elif self.loss_type == 'cross_entropy':
            self.criterion = nn.CrossEntropyLoss(weight=torch.tensor([self.class_weights['normal'], self.class_weights['threat']]))
        else:
            raise ValueError(f"Unsupported loss type: {loss_type}")

    def forward(self, preds: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
        """
        Calculates loss between predictions and targets.
        """
        # Squeeze in case of shape mismatch
        preds = preds.squeeze()
        targets = targets.squeeze().float()
        
        if self.loss_type == 'cross_entropy':
            targets = targets.long()
            
        return self.criterion(preds, targets)
