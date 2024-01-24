from .logistic_model import backward_regression as fit_logistic_regression
from .linear_model import backward_regression as fit_linear_regression


__all__ = [
    'fit_logistic_regression',
    'fit_linear_regression'
]