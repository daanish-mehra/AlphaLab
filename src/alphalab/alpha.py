from typing import Callable, Dict, List, Any, Optional
import pandas as pd


class Alpha:
    """Basic alpha strategy - takes a universe of assets and generates signals."""
    
    def __init__(
        self,
        name: str,
        signal_fn: Callable[[List[str]], Dict[str, float]],
        universe: Optional[List[str]] = None
    ):
        self.name = name
        self.signal_fn = signal_fn
        # Default to empty list if no universe given
        self.universe = universe or []
    
    def run(self, universe: Optional[List[str]] = None) -> pd.DataFrame:
        """Run the alpha and get signals back as a DataFrame."""
        # Can override the default universe if needed
        if universe is not None:
            assets = universe
        else:
            assets = self.universe
        
        if not assets:
            raise ValueError("Universe must be provided")
        
        # Get signals from the function
        signal_dict = self.signal_fn(assets)
        
        # Convert to DataFrame - easier to work with than a dict
        df = pd.DataFrame.from_dict(signal_dict, orient='index', columns=['signal'])
        df.index.name = 'asset'
        
        return df
    
    def metadata(self) -> Dict[str, Any]:
        """Just some basic info about the strategy."""
        return {
            "name": self.name,
            "universe_size": len(self.universe),
            "has_universe": len(self.universe) > 0
        }

