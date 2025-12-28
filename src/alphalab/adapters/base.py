from abc import ABC, abstractmethod
from typing import Any, Dict
from alphalab.alpha import Alpha


class BaseAdapter(ABC):
    """Base class for connecting to different backtesting engines.
    
    The idea here is that different backtesting platforms (QuantConnect, Zipline,
    etc.) all have different APIs. This adapter pattern lets us plug any of them
    into AlphaLab without changing the core code. Just inherit from this class
    and implement run_alpha() for whatever platform you're using.
    """
    
    @abstractmethod
    def run_alpha(self, alpha: Alpha) -> Dict[str, Any]:
        """Run an alpha through your backtesting engine.
        
        This is the method you need to implement. It should take an Alpha object,
        run it through whatever backtesting engine you're using, and return the
        results as a dictionary. What goes in that dict is up to you - usually
        things like Sharpe ratio, returns, drawdown, etc.
        
        Args:
            alpha: The Alpha strategy to backtest
        
        Returns:
            A dict with backtest results. The structure is flexible - depends
            on what your backtesting engine gives you.
        """
        raise NotImplementedError("Subclasses must implement run_alpha()")

