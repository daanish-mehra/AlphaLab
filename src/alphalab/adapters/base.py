from abc import ABC, abstractmethod
from typing import Any, Dict
from alphalab.alpha import Alpha


class BaseAdapter(ABC):
    """Base class for connecting to different backtesting engines."""
    
    @abstractmethod
    def run_alpha(self, alpha: Alpha) -> Dict[str, Any]:
        """Implement this to run an alpha through your backtesting engine."""
        raise NotImplementedError("Subclasses must implement run_alpha()")

