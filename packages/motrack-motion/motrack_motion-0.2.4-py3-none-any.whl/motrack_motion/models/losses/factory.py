"""
Loss function factory method.
"""
from torch import nn

from motrack_motion.models.losses.giou import HybridGaussianNLLLossGIoU, HybridL1GIoU


def factory_loss_function(name: str, params: dict) -> nn.Module:
    """
    Crates loss function based on give name and parameters.

    Args:
        name: Loss function name
        params: Loss function parameters

    Returns:
        Loss function object.
    """
    catalog = {
        'mse': nn.MSELoss,
        'huber': nn.HuberLoss,
        'gaussian_nllloss': nn.GaussianNLLLoss,
        'hybrid_l1_giou': HybridL1GIoU,
        'hybrid_gaussian_nllloss_giou': HybridGaussianNLLLossGIoU
    }

    name = name.lower()
    if name not in catalog:
        raise KeyError(f'Unknown loss name "{name}". Available: {list(catalog.keys())}.')

    return catalog[name](**params)
