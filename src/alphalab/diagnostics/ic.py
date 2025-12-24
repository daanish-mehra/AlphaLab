from typing import Union
import pandas as pd
import numpy as np


def information_coefficient(
    signals: Union[pd.Series, np.ndarray],
    returns: Union[pd.Series, np.ndarray]
) -> float:
    """Calculate IC - basically just correlation between signals and returns."""
    # Convert numpy arrays to Series if needed
    if isinstance(signals, np.ndarray):
        signals = pd.Series(signals)
    if isinstance(returns, np.ndarray):
        returns = pd.Series(returns)
    
    if len(signals) != len(returns):
        raise ValueError("signals and returns must have the same length")
    
    ic = signals.corr(returns)
    
    # Can't compute correlation if everything is the same (NaN), return 0
    if pd.isna(ic):
        return 0.0
    
    return float(ic)

