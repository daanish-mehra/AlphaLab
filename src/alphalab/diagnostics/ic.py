from typing import Union
import pandas as pd
import numpy as np


def information_coefficient(
    signals: Union[pd.Series, np.ndarray],
    returns: Union[pd.Series, np.ndarray]
) -> float:
    """Calculate Information Coefficient - basically how well your signals predicted returns.
    
    IC is just the correlation between what you predicted (signals) and what actually
    happened (returns). Higher is better - typically you want IC > 0.05 to consider
    a strategy decent. It's a pretty standard metric in quant finance.
    
    Args:
        signals: Your predicted signals - can be Series or numpy array, doesn't matter
        returns: What actually happened - must be the same length as signals
    
    Returns:
        The IC value (float between -1 and 1). Returns 0.0 if correlation can't be
        computed (happens when all values are the same).
    
    Raises:
        ValueError: If the lengths don't match - can't compare them then
    
    Example:
        >>> import pandas as pd
        >>> signals = pd.Series([0.1, -0.2, 0.3, -0.1])
        >>> returns = pd.Series([0.08, -0.15, 0.28, -0.05])
        >>> ic = information_coefficient(signals, returns)
        >>> print(f"IC: {ic:.3f}")
        IC: 0.995
    """
    # Convert numpy arrays to Series if needed - easier to work with Series
    if isinstance(signals, np.ndarray):
        signals = pd.Series(signals)
    
    if isinstance(returns, np.ndarray):
        returns = pd.Series(returns)
    
    # Can't compute correlation if lengths don't match
    if len(signals) != len(returns):
        raise ValueError("signals and returns must have the same length")
    
    # Calculate correlation - this is the IC
    ic_value = signals.corr(returns)
    
    # Edge case: if everything is the same value, correlation is NaN
    # Just return 0 in that case since there's no predictive power
    if pd.isna(ic_value):
        return 0.0
    
    return float(ic_value)

