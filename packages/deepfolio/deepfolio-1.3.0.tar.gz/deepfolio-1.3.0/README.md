<div align=center>
<img src="assets/deepfolio.png" width="45%" loc>

[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.15-red)](https://tensorflow.org/)
![PyPI - Version](https://img.shields.io/pypi/v/deepfolio)
[![License](https://img.shields.io/badge/License-BSD_2--Clause-orange.svg)](https://opensource.org/licenses/BSD-2-Clause)
![Python versions](https://img.shields.io/badge/python-3.6%2B-green)
![PyPI downloads](https://img.shields.io/pypi/dm/deepfolio)  

</div>

**DeepFolio** is a Python library for real-time portfolio optimization built on top of Google's TensorFlow platform. It combines optimization techniques (both convex and non-convex) with deep learning approaches to provide a powerful toolkit for investment professionals and researchers.

## Installation

Install the package using pip:

```bash
pip install --upgrade deepfolio
```

## Features

- Differentiable portfolio optimization
- Real-time optimization
- Robust and multi-period optimization
- Multi-asset class support
- Backtesting system
- Risk management tools
- Factor model integration
- Automated hyperparameter tuning (Backed by Optuna)
- Trade execution simulation
- Event-driven rebalancing
- Comprehensive reporting
- Sentiment analysis integration
- Tax-aware optimization
- Interactive visualization dashboard

## Installation

```bash
pip install -U deepfolio
```

## Quick Start

```python
from deepfolio.models import DiffOptPortfolio
from deepfolio.optimizers import CustomOptimizer
from deepfolio import Backtester

# Initialize the model
model = DiffOptPortfolio(input_dim=50, n_assets=10, hidden_dim=64)

# Create an optimizer
optimizer = CustomOptimizer(model.parameters())

# Load your data
features, returns = load_your_data()

# Create a backtester
backtester = Backtester(model, {'features': features, 'returns': returns})

# Run backtesting
backtester.run()

# Get results
results = backtester.get_results()
print(f"Sharpe Ratio: {results['sharpe_ratio']}")
print(f"Max Drawdown: {results['max_drawdown']}")
```

## Advanced Usage

### Real-time Optimization

```python
from deepfolio.models import RealtimeOptimizer
from deepfolio.data import DataSource

data_source = DataSource(api_key="your_api_key")
optimizer = RealtimeOptimizer(model, data_source)
optimizer.start()
```

### Multi-Asset Optimization

```python
from deepfolio.models import MultiAssetDiffOptPortfolio

asset_classes = ['stocks', 'bonds', 'commodities']
input_dims = {'stocks': 50, 'bonds': 30, 'commodities': 20}
hidden_dims = {'stocks': 64, 'bonds': 32, 'commodities': 32}
model = MultiAssetDiffOptPortfolio(asset_classes, input_dims, hidden_dims)
```

### Tax-Aware Optimization

```python
from deepfolio.optimizers import TaxOptimizer

tax_optimizer = TaxOptimizer()
optimal_trades = tax_optimizer.optimize(current_portfolio, target_weights, prices, cost_basis, holding_period)
```

### Interactive Dashboard

```python
from deepfolio.utils import PortfolioDashboard

dashboard = PortfolioDashboard(portfolio_data, benchmark_data)
dashboard.run()
```

## Documentation

For detailed documentation, please visit our [documentation site](https://diffopt-portfolio.readthedocs.io).

## Contributing

We welcome contributions! Please see our [contributing guidelines](CONTRIBUTING.md) for more details.


## License

This project is licensed under the BSD-2-Clause License- see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- This package leverages the power of TensorFlow for efficient portfolio optimization.
- Thanks to the financial machine learning community for inspiring many of the implemented methods.




