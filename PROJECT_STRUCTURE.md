# AlphaLab Project Structure

## Overview
AlphaLab is a Python framework for developing and testing alpha trading strategies. The project uses a modern Python package structure with setuptools configuration.

## Project Structure

```
AlphaLab/
├── README.md                          # Project documentation with description and quickstart
├── LICENSE                            # MIT License
├── .gitignore                         # Git ignore file (excludes .venv, __pycache__, etc.)
├── pyproject.toml                     # Modern Python project configuration (setuptools, pytest)
├── requirements.txt                   # Python dependencies (numpy, pandas, pytest)
│
├── src/
│   └── alphalab/                     # Main package
│       ├── __init__.py               # Package init, exports Alpha class
│       ├── alpha.py                  # Alpha class - core strategy representation
│       │                             #   - Attributes: name (str), signal_fn (Callable), universe (List[str])
│       │                             #   - Methods: run() -> pd.DataFrame, metadata() -> Dict[str, Any]
│       │
│       ├── adapters/                 # Backtesting engine adapters
│       │   ├── __init__.py           # Exports BaseAdapter
│       │   └── base.py               # BaseAdapter abstract base class
│       │                             #   - Abstract method: run_alpha(alpha) -> Dict[str, Any]
│       │
│       └── diagnostics/              # Performance evaluation tools
│           ├── __init__.py           # Exports information_coefficient
│           └── ic.py                 # Information Coefficient calculation
│                                     #   - Function: information_coefficient(signals, returns) -> float
│
├── tests/
│   └── test_alpha.py                 # Unit tests for Alpha class
│                                     #   - test_alpha_basic: initialization, attributes, method return types
│                                     #   - test_alpha_initialization: basic initialization test
│                                     #   - test_alpha_run: run() method test
│                                     #   - test_alpha_run_with_custom_universe: custom universe test
│                                     #   - test_alpha_run_no_universe: error handling test
│                                     #   - test_alpha_metadata: metadata() method test
│
└── notebooks/
    └── quickstart.ipynb              # Example usage notebook
                                     #   - Shows basic Alpha creation and metadata() call
```

## Key Components

### Alpha Class (`src/alphalab/alpha.py`)
- **Purpose**: Represents an alpha trading strategy
- **Attributes**:
  - `name`: str - Name of the strategy
  - `signal_fn`: Callable[[List[str]], Dict[str, float]] - Function that generates signals
  - `universe`: Optional[List[str]] - List of asset identifiers
- **Methods**:
  - `run(universe: Optional[List[str]] = None) -> pd.DataFrame`: Generates signals, returns DataFrame with assets as index and 'signal' column
  - `metadata() -> Dict[str, Any]`: Returns metadata about the strategy

### BaseAdapter (`src/alphalab/adapters/base.py`)
- **Purpose**: Abstract base class for backtesting engine adapters
- **Methods**:
  - `run_alpha(alpha: Alpha) -> Dict[str, Any]`: Abstract method to run an alpha through a backtesting engine

### Information Coefficient (`src/alphalab/diagnostics/ic.py`)
- **Purpose**: Calculate Information Coefficient (correlation between signals and returns)
- **Function**: `information_coefficient(signals: Union[pd.Series, np.ndarray], returns: Union[pd.Series, np.ndarray]) -> float`

## Dependencies
- **numpy** >= 1.20.0
- **pandas** >= 1.3.0
- **pytest** >= 7.0.0 (for testing)

## Configuration Files

### pyproject.toml
- Modern setuptools build configuration
- Package metadata (name: "alphalab", version: "0.1.0")
- pytest configuration with `pythonpath = ["src"]`
- Package structure: src layout with package-dir mapping

### requirements.txt
- Runtime dependencies: numpy, pandas
- Development dependencies: pytest

## Test Configuration
- Pytest configured in pyproject.toml
- Test path: `tests/`
- Python path includes `src/` directory for imports
- All tests use type hints and follow pytest conventions

## Development Setup
- Virtual environment: `.venv/` (excluded from git)
- Package installation: `pip install -e .` (editable mode)
- Run tests: `pytest tests/`
- Python version: >= 3.8

## Code Style
- All classes and functions include type hints
- All classes and functions include docstrings
- Follows Python best practices and PEP 8 style guide