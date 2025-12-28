from typing import Callable, Dict, List, Any, Optional
import pandas as pd


class Alpha:
    """A trading strategy that generates signals for assets.
    
    This is the main class you'll use to create and run alpha strategies.
    Just give it a name, a function that generates signals, and optionally
    a universe of assets to trade.
    """
    
    def __init__(
        self,
        name: str,
        signal_fn: Callable[[List[str]], Dict[str, float]],
        universe: Optional[List[str]] = None
    ):
        """Create a new alpha strategy.
        
        Args:
            name: What you want to call this strategy
            signal_fn: Your signal function - takes a list of tickers, returns a dict
                with ticker -> signal value pairs
            universe: Optional list of assets. If you don't set it here, you can
                pass it later when you call run()
        """
        self.name = name
        self.signal_fn = signal_fn
        
        # If no universe was provided, start with an empty list
        # The user will need to pass one to run() later
        if universe is None:
            self.universe = []
        else:
            self.universe = universe
    
    def run(self, universe: Optional[List[str]] = None) -> pd.DataFrame:
        """Run the alpha and get back signals as a DataFrame.
        
        This is where the magic happens - it calls your signal function for
        all the assets in the universe and gives you back a nice DataFrame
        you can work with.
        
        Args:
            universe: Optional - if you pass this, it uses this instead of
                the one you set when creating the Alpha. Useful for testing
                different universes without creating a new Alpha object.
        
        Returns:
            A DataFrame with tickers as the index and signal values in a
            column called 'signal'. Easy to work with!
        
        Raises:
            ValueError: If you didn't provide a universe anywhere (not here
                and not when you created the Alpha).
        """
        # Figure out which universe to use - the one passed in takes priority
        if universe is not None:
            assets_to_process = universe
        else:
            assets_to_process = self.universe
        
        # Can't do anything without at least one asset
        if len(assets_to_process) == 0:
            raise ValueError("Universe must be provided")
        
        # Run the signal function - this gives us a dict of {ticker: signal_value}
        signals_by_asset = self.signal_fn(assets_to_process)
        
        # Convert to DataFrame - much easier to work with than a dict
        # Setting orient = 'index' makes the tickers the row index, which is what we want
        result_df = pd.DataFrame.from_dict(
            signals_by_asset,
            orient = 'index',
            columns = ['signal']
        )
        
        # Give the index a nice name
        result_df.index.name = 'asset'
        
        return result_df
    
    def metadata(self) -> Dict[str, Any]:
        """Get some basic info about this strategy.
        
        Just returns a dict with the name, how many assets are in the universe,
        and whether a universe was actually set. Handy for debugging or logging.
        
        Returns:
            Dict with 'name', 'universe_size', and 'has_universe' keys
        """
        # Check if we have a universe set (might be empty)
        has_universe_set = len(self.universe) > 0
        
        return {
            "name": self.name,
            "universe_size": len(self.universe),
            "has_universe": has_universe_set
        }

