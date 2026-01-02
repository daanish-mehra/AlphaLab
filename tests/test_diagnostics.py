"""Tests for diagnostic functions - making sure they work correctly."""

import pytest
import pandas as pd
import numpy as np
from alphalab.diagnostics import information_coefficient, sharpe_ratio


def test_sharpe_ratio_basic():
    """Test that sharpe_ratio actually calculates something reasonable."""
    # Simple test with some positive returns
    returns = pd.Series([0.01, 0.02, -0.01, 0.015, 0.01])
    sharpe = sharpe_ratio(returns, risk_free_rate = 0.0, periods_per_year = 252)
    
    assert isinstance(sharpe, float)
    assert sharpe > 0  # Should be positive since we have net positive returns


def test_sharpe_ratio_with_risk_free_rate():
    """Test that sharpe_ratio works when you include a risk-free rate."""
    returns = pd.Series([0.01, 0.02, 0.01, 0.015, 0.01])
    sharpe = sharpe_ratio(returns, risk_free_rate = 0.05, periods_per_year = 252)
    
    assert isinstance(sharpe, float)


def test_sharpe_ratio_zero_volatility():
    """Test that sharpe_ratio handles the edge case where all returns are the same."""
    # If everything is the same, there's no volatility - Sharpe should be 0
    returns = pd.Series([0.01, 0.01, 0.01, 0.01, 0.01])
    sharpe = sharpe_ratio(returns)
    
    assert sharpe == 0.0


def test_sharpe_ratio_empty():
    """Test that sharpe_ratio doesn't crash when given empty returns."""
    returns = pd.Series([])
    sharpe = sharpe_ratio(returns)
    
    assert sharpe == 0.0


def test_sharpe_ratio_numpy_array():
    """Test that sharpe_ratio works with numpy arrays, not just pandas Series."""
    returns = np.array([0.01, 0.02, -0.01, 0.015, 0.01])
    sharpe = sharpe_ratio(returns)
    
    assert isinstance(sharpe, float)
    assert sharpe > 0

