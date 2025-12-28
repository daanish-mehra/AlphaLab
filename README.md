# AlphaLab

A framework for developing and testing alpha trading strategies.

> **Note**: This project has been refactored for clarity and readability, with improved code structure and documentation.

## Description

AlphaLab provides a simple and extensible framework for creating, testing, and evaluating alpha trading strategies. It offers:

- **Alpha Class**: A clean interface for defining trading signals
- **Adapter Pattern**: Pluggable backtesting engine support
- **Diagnostics**: Tools for evaluating strategy performance (e.g., Information Coefficient)

## Installation

```bash
pip install -r requirements.txt
```

Or install in development mode:

```bash
pip install -e .
```

## Quickstart

```python
from alphalab import Alpha

# Define a simple signal function
def my_signal_fn(universe):
    """Generate signals for each asset in the universe."""
    # In practice, this would use real data analysis
    return {asset: 0.1 for asset in universe}

# Create an alpha strategy
alpha = Alpha(
    name="my_first_alpha",
    signal_fn=my_signal_fn,
    universe=["AAPL", "GOOGL", "MSFT", "AMZN"]
)

# Run the strategy
signals = alpha.run()
print(signals)

# Get metadata
metadata = alpha.metadata()
print(metadata)
```

## Project Structure

```
alphalab/
├── src/
│   └── alphalab/
│       ├── alpha.py          # Alpha class
│       ├── adapters/         # Backtesting engine adapters
│       └── diagnostics/      # Performance evaluation tools
├── tests/                    # Unit tests
└── notebooks/                # Example notebooks
```

## Testing

Run tests with pytest:

```bash
pytest
```

## License

MIT License - see LICENSE file for details.
