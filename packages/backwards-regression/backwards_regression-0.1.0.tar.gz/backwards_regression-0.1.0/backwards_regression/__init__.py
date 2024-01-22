from .logistic_model import backward_regression as fit_logistic
from .linear_model import backward_regression as fit_linear


__all__ = [
    'fit_logistic',
    'fit_linear'
]