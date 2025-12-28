"""Tests for the Alpha class - making sure everything works as expected."""

import pytest
import pandas as pd
from alphalab.alpha import Alpha


def test_alpha_basic():
    """Basic smoke test - can we create an Alpha and does it have the right stuff?"""
    # Make a simple signal function for testing - just returns zeros
    def dummy_signal_fn(universe):
        return {asset: 0.0 for asset in universe}
    
    # Create an alpha instance
    alpha = Alpha(
        name = "test_alpha",
        signal_fn = dummy_signal_fn,
        universe = ["AAPL", "GOOGL"]
    )
    
    # Check that all the attributes exist and are the right type
    assert hasattr(alpha, 'name')
    assert hasattr(alpha, 'signal_fn')
    assert hasattr(alpha, 'universe')
    assert isinstance(alpha.name, str)
    assert callable(alpha.signal_fn)
    assert isinstance(alpha.universe, list)
    
    # Test that run() gives us back a DataFrame
    result = alpha.run()
    assert isinstance(result, pd.DataFrame)
    
    # Test that metadata() gives us back a dict
    metadata = alpha.metadata()
    assert isinstance(metadata, dict)


def test_alpha_initialization():
    """Make sure Alpha stores everything we pass to it correctly."""
    def dummy_signal_fn(universe):
        return {asset: 0.1 for asset in universe}
    
    alpha = Alpha(
        name = "test_alpha",
        signal_fn = dummy_signal_fn,
        universe = ["AAPL", "GOOGL", "MSFT"]
    )
    
    # Everything should be stored as expected
    assert alpha.name == "test_alpha"
    assert alpha.universe == ["AAPL", "GOOGL", "MSFT"]
    assert callable(alpha.signal_fn)


def test_alpha_run():
    """Test that run() actually works and gives us back signals in the right format."""
    def dummy_signal_fn(universe):
        return {asset: 0.1 for asset in universe}
    
    alpha = Alpha(
        name = "test_alpha",
        signal_fn = dummy_signal_fn,
        universe = ["AAPL", "GOOGL"]
    )
    
    # Run it and see what we get
    signals_df = alpha.run()
    assert isinstance(signals_df, pd.DataFrame)
    
    # Check the structure - tickers should be the index
    assert signals_df.index.tolist() == ["AAPL", "GOOGL"]
    
    # And the signal values should be what we expect
    assert signals_df.loc["AAPL", "signal"] == 0.1
    assert signals_df.loc["GOOGL", "signal"] == 0.1


def test_alpha_run_with_custom_universe():
    """Test that we can override the universe when calling run()."""
    def dummy_signal_fn(universe):
        return {asset: 0.5 for asset in universe}
    
    # Create an alpha with one universe
    alpha = Alpha(
        name = "test_alpha",
        signal_fn = dummy_signal_fn,
        universe = ["AAPL"]
    )
    
    # But then pass a completely different one to run()
    signals_df = alpha.run(universe = ["TSLA", "NVDA"])
    assert isinstance(signals_df, pd.DataFrame)
    
    # Should use the one we passed in, not the default
    assert signals_df.index.tolist() == ["TSLA", "NVDA"]
    assert signals_df.loc["TSLA", "signal"] == 0.5
    assert signals_df.loc["NVDA", "signal"] == 0.5


def test_alpha_run_no_universe():
    """Test that run() properly errors out when there's no universe to work with."""
    def dummy_signal_fn(universe):
        return {}
    
    # Create an alpha without a universe
    alpha = Alpha(
        name = "test_alpha",
        signal_fn = dummy_signal_fn,
        universe = None
    )
    
    # This should fail - can't run without a universe
    with pytest.raises(ValueError, match="Universe must be provided"):
        alpha.run()


def test_alpha_metadata():
    """Test that metadata() gives us back the info we expect."""
    def dummy_signal_fn(universe):
        return {}
    
    alpha = Alpha(
        name = "test_alpha",
        signal_fn = dummy_signal_fn,
        universe = ["AAPL", "GOOGL", "MSFT"]
    )
    
    # Get the metadata and check each field
    metadata = alpha.metadata()
    assert metadata["name"] == "test_alpha"
    assert metadata["universe_size"] == 3
    assert metadata["has_universe"] is True

