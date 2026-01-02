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


def sharpe_ratio(
    returns: Union[pd.Series, np.ndarray],
    risk_free_rate: float = 0.0,
    periods_per_year: int = 252
) -> float:
    """Calculate Sharpe ratio - basically how much return you're getting per unit of risk.
    
    Sharpe ratio is a standard way to measure risk-adjusted returns. It tells you if
    your strategy is actually good or if you're just taking on more risk. Higher is
    better - typically you want Sharpe > 1.0 to consider a strategy decent. It's
    just (mean return - risk free rate) / standard deviation, then annualized.
    
    Args:
        returns: Your strategy returns - can be Series or numpy array
        risk_free_rate: Risk-free rate (default 0.0, but you can use treasury rate if you want)
        periods_per_year: How many periods make up a year (252 for daily, 12 for monthly, etc.)
    
    Returns:
        Annualized Sharpe ratio. Returns 0.0 if there's no volatility (can't divide by zero).
    
    Example:
        >>> import pandas as pd
        >>> returns = pd.Series([0.01, 0.02, -0.01, 0.015, 0.01])
        >>> sharpe = sharpe_ratio(returns, risk_free_rate = 0.02, periods_per_year = 252)
        >>> print(f"Sharpe: {sharpe:.3f}")
    """
    # Convert numpy arrays to Series if needed
    if isinstance(returns, np.ndarray):
        returns = pd.Series(returns)
    
    # Can't calculate anything with no data
    if len(returns) == 0:
        return 0.0
    
    # Get the mean and standard deviation of returns
    mean_return = returns.mean()
    std_return = returns.std()
    
    # If there's no volatility, Sharpe is undefined - just return 0
    if std_return == 0 or pd.isna(std_return):
        return 0.0
    
    # Calculate excess return (above risk-free rate)
    # Need to adjust risk-free rate to match the period frequency
    excess_return = mean_return - (risk_free_rate / periods_per_year)
    
    # Annualize the Sharpe ratio by multiplying by sqrt of periods per year
    sharpe = excess_return / std_return * np.sqrt(periods_per_year)
    
    return float(sharpe)

