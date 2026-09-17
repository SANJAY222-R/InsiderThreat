import torch
from typing import Dict, Any, List

try:
    import torchmetrics
except Exception:
    torchmetrics = None

try:
    from sklearn import metrics as sk_metrics
except Exception:
    sk_metrics = None


class ModelEvaluator:
    """
    Validation pipeline with torchmetrics and sklearn fallback.
    Tracks Loss, Accuracy, Precision, Recall, F1, ROC-AUC.
    """
    def __init__(self, device: torch.device) -> None:
        self.device = device
        self._all_preds: List[torch.Tensor] = []
        self._all_targets: List[torch.Tensor] = []

        if torchmetrics is not None:
            self.metrics: Any = torchmetrics.MetricCollection({
                'accuracy': torchmetrics.Accuracy(task='binary'),
                'precision': torchmetrics.Precision(task='binary'),
                'recall': torchmetrics.Recall(task='binary'),
                'f1': torchmetrics.F1Score(task='binary'),
                'auroc': torchmetrics.AUROC(task='binary')
            }).to(self.device)
            self.conf_mat: Any = torchmetrics.ConfusionMatrix(task='binary', num_classes=2).to(self.device)
        else:
            self.metrics: Any = None
            self.conf_mat: Any = None

    def update(self, preds: torch.Tensor, targets: torch.Tensor) -> None:
        preds_flat = preds.squeeze().float()
        targets_flat = targets.squeeze().long()

        if torchmetrics is not None and self.metrics is not None:
            self.metrics.update(preds_flat, targets_flat)
            probs = torch.sigmoid(preds_flat) if not torch.all((preds_flat >= 0) & (preds_flat <= 1)) else preds_flat
            if self.conf_mat is not None:
                self.conf_mat.update(probs, targets_flat)
        else:
            probs = torch.sigmoid(preds_flat) if not torch.all((preds_flat >= 0) & (preds_flat <= 1)) else preds_flat
            self._all_preds.append(probs.detach().cpu())
            self._all_targets.append(targets_flat.detach().cpu())

    def compute(self) -> Dict[str, float]:
        if torchmetrics is not None and self.metrics is not None:
            res = self.metrics.compute()
            return {k: v.item() for k, v in res.items()}

        if not self._all_preds or sk_metrics is None:
            return {'accuracy': 0.0, 'precision': 0.0, 'recall': 0.0, 'f1': 0.0, 'auroc': 0.0}

        y_prob = torch.cat(self._all_preds).numpy()
        y_true = torch.cat(self._all_targets).numpy()
        y_pred = (y_prob >= 0.5).astype(int)

        acc = float(sk_metrics.accuracy_score(y_true, y_pred))
        prec = float(sk_metrics.precision_score(y_true, y_pred, zero_division="warn"))
        rec = float(sk_metrics.recall_score(y_true, y_pred, zero_division="warn"))
        f1 = float(sk_metrics.f1_score(y_true, y_pred, zero_division="warn"))

        try:
            auroc = float(sk_metrics.roc_auc_score(y_true, y_prob)) if len(set(y_true)) > 1 else 0.5
        except Exception:
            auroc = 0.5

        return {
            'accuracy': acc,
            'precision': prec,
            'recall': rec,
            'f1': f1,
            'auroc': auroc
        }

    def get_confusion_matrix(self) -> torch.Tensor:
        if torchmetrics is not None and self.conf_mat is not None:
            return self.conf_mat.compute()

        if not self._all_preds or sk_metrics is None:
            return torch.zeros((2, 2))

        y_prob = torch.cat(self._all_preds).numpy()
        y_true = torch.cat(self._all_targets).numpy()
        y_pred = (y_prob >= 0.5).astype(int)
        cm = sk_metrics.confusion_matrix(y_true, y_pred, labels=[0, 1])
        return torch.tensor(cm)

    def reset(self) -> None:
        self._all_preds.clear()
        self._all_targets.clear()
        if torchmetrics is not None and self.metrics is not None:
            self.metrics.reset()
        if torchmetrics is not None and self.conf_mat is not None:
            self.conf_mat.reset()
