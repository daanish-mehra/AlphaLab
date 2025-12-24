"""Unit tests for the Alpha class."""

import pytest
import pandas as pd
from typing import Dict, Any
from alphalab.alpha import Alpha


def test_alpha_basic():
    """
    Basic test to ensure Alpha class can be initialized,
    attributes exist, and methods return correct types.
    """
    def dummy_signal_fn(universe):
        return {asset: 0.0 for asset in universe}
    
    # Test 1: Alpha object can be initialized
    alpha = Alpha(
        name="test_alpha",
        signal_fn=dummy_signal_fn,
        universe=["AAPL", "GOOGL"]
    )
    
    # Test 2: Attributes exist
    assert hasattr(alpha, 'name')
    assert hasattr(alpha, 'signal_fn')
    assert hasattr(alpha, 'universe')
    assert isinstance(alpha.name, str)
    assert callable(alpha.signal_fn)
    assert isinstance(alpha.universe, list)
    
    # Test 3: run() returns correct type (pd.DataFrame)
    result = alpha.run()
    assert isinstance(result, pd.DataFrame)
    
    # Test 4: metadata() returns correct type (Dict[str, Any])
    metadata = alpha.metadata()
    assert isinstance(metadata, dict)


def test_alpha_initialization():
    """Test Alpha class initialization."""
    def dummy_signal_fn(universe):
        return {asset: 0.1 for asset in universe}
    
    alpha = Alpha(
        name="test_alpha",
        signal_fn=dummy_signal_fn,
        universe=["AAPL", "GOOGL", "MSFT"]
    )
    
    assert alpha.name == "test_alpha"
    assert alpha.universe == ["AAPL", "GOOGL", "MSFT"]
    assert callable(alpha.signal_fn)


def test_alpha_run():
    """Test Alpha.run() method."""
    def dummy_signal_fn(universe):
        return {asset: 0.1 for asset in universe}
    
    alpha = Alpha(
        name="test_alpha",
        signal_fn=dummy_signal_fn,
        universe=["AAPL", "GOOGL"]
    )
    
    signals_df = alpha.run()
    assert isinstance(signals_df, pd.DataFrame)
    assert signals_df.index.tolist() == ["AAPL", "GOOGL"]
    assert signals_df.loc["AAPL", "signal"] == 0.1
    assert signals_df.loc["GOOGL", "signal"] == 0.1


def test_alpha_run_with_custom_universe():
    """Test Alpha.run() with custom universe."""
    def dummy_signal_fn(universe):
        return {asset: 0.5 for asset in universe}
    
    alpha = Alpha(
        name="test_alpha",
        signal_fn=dummy_signal_fn,
        universe=["AAPL"]
    )
    
    signals_df = alpha.run(universe=["TSLA", "NVDA"])
    assert isinstance(signals_df, pd.DataFrame)
    assert signals_df.index.tolist() == ["TSLA", "NVDA"]
    assert signals_df.loc["TSLA", "signal"] == 0.5
    assert signals_df.loc["NVDA", "signal"] == 0.5


def test_alpha_run_no_universe():
    """Test Alpha.run() raises error when no universe provided."""
    def dummy_signal_fn(universe):
        return {}
    
    alpha = Alpha(
        name="test_alpha",
        signal_fn=dummy_signal_fn,
        universe=None
    )
    
    with pytest.raises(ValueError, match="Universe must be provided"):
        alpha.run()


def test_alpha_metadata():
    """Test Alpha.metadata() method."""
    def dummy_signal_fn(universe):
        return {}
    
    alpha = Alpha(
        name="test_alpha",
        signal_fn=dummy_signal_fn,
        universe=["AAPL", "GOOGL", "MSFT"]
    )
    
    metadata = alpha.metadata()
    assert metadata["name"] == "test_alpha"
    assert metadata["universe_size"] == 3
    assert metadata["has_universe"] is True

