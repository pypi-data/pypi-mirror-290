"""
This module is for ML model metric calculators
"""

import numpy as np
import torch
from torch.nn import functional as F


def do_softmax(pred):
    """
    Pass the prediction through a softmax filter
    """
    return torch.argmax(F.softmax(pred, dim=1), dim=1)


def pixel_accuracy(pred, gt):
    with torch.no_grad():
        match = torch.eq(pred, torch.amax(gt, dim=1)).int()
    return float(match.sum()) / float(match.numel())


def softmaxed_pixel_accuracy(pred, gt):
    softmax_pred = do_softmax(pred)
    return pixel_accuracy(softmax_pred, gt)


class MeanIouCalculator:
    def __init__(self, num_classes, eps=1.0e-10):
        self.num_classes = num_classes
        self.eps = eps

    def to_contiguous(self, array):
        return array.contiguous().view(-1)

    def mean_iou(self, pred, gt):
        with torch.no_grad():
            gt = torch.amax(gt, dim=1)
            pred = self.to_contiguous(pred)
            gt = self.to_contiguous(gt)

            iou_per_class = []
            for c in range(self.num_classes):
                match_pred = pred == c
                match_gt = gt == c
                if match_gt.long().sum().item() == 0:
                    iou_per_class.append(np.nan)
                else:
                    intersect = (
                        torch.logical_and(match_pred, match_gt).sum().float().item()
                    )
                    union = torch.logical_or(match_pred, match_gt).sum().float().item()

                    iou = (intersect + self.eps) / (union + self.eps)
                    iou_per_class.append(iou)
            return np.nanmean(iou_per_class)

    def __call__(self, pred, gt):
        softmax_pred = do_softmax(pred)
        return self.mean_iou(softmax_pred, gt)


def basic_accuracy(pred, gt):
    _, predicted = torch.max(pred, 1)
    return (predicted == gt).sum().item()


class TorchLossCalculator:
    """
    A calculator for model metrics
    """

    def __init__(
        self,
        loss_func,
        use_argmax_loss: bool = False,
    ):
        self.loss_func = loss_func
        self.armgax_loss = use_argmax_loss

    def __call__(self, pred, gt):
        if self.armgax_loss:
            return self.loss_func(pred, torch.argmax(gt, dim=1))
        return self.loss_func(pred, gt)
