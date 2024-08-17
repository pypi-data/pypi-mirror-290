<!-- <p align="center">
<img src="https://github.com/luochang212/flameai/raw/main/docs/_static/flame.jpeg" alt="logo" width=88%>
</p> -->


# 🔥 FlameAI

[![License](https://img.shields.io/github/license/luochang212/flameai)](https://github.com/luochang212/flameai)
[![PyPI](https://img.shields.io/pypi/v/flameai.svg?logo=python)](https://pypi.python.org/pypi/flameai)
[![GitHub](https://img.shields.io/github/v/release/luochang212/flameai?logo=github&sort=semver)](https://github.com/luochang212/flameai)
[![CI](https://github.com/luochang212/flameai/workflows/CI/badge.svg)](https://github.com/luochang212/flameai/actions?query=workflow:CI)
[![Downloads](https://static.pepy.tech/personalized-badge/flameai?period=total&units=international_system&left_color=grey&right_color=green&left_text=Downloads)](https://pepy.tech/project/flameai)

Python Deep Learning Toolkit.

## Installation

Install the package: 

```bash
pip install flameai
```

Update the package:

```bash
python3 -m pip install --upgrade pip
pip3 install --upgrade flameai
```

## Example

Evaluate the performance of a binary classification model:

```python
# simple.py
import flameai

y_true = [0, 0, 0, 1, 0, 1, 0, 1, 1, 0]
y_pred = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

flameai.eval_binary(y_true, y_pred, threshold=0.5)
```

```bash
$ python examples/simple.py
threshold: 0.50000
accuracy: 0.70000
precision: 0.60000
recall: 0.75000
f1_score: 0.66667
auc: 0.70833
cross-entropy loss: 4.03816
True Positive (TP): 3
True Negative (TN): 4
False Positive (FP): 2
False Negative (FN): 1
confusion matrix:
[[4 2]
 [1 3]]
```

More examples: [examples](/examples/)

## Test Locally

Create a conda environment:

```bash
# Create env
mamba create -n python_3_10 python=3.10

# Activate env
conda activate python_3_10

# Check envs
conda info --envs

# Deactivate env
conda deactivate

# Remove env
conda env remove --name python_3_10
```

Install the package from source (or local wheel):

```bash
# Check if flameai has been installed
pip list | grep flameai

# Install from source
pip install -e .

# Or install from local wheel
# `pip install dist/flameai-[VERSION]-py3-none-any.whl`

# Uninstall
pip uninstall flameai

# Reinstall
pip uninstall flameai -y && pip install -e .
```

Test:

```bash
# Install pytest
pip install pytest

# Run tests
pytest

# Install nox
pip install nox

# Run nox
nox
```

Lint:

```bash
# Install flake8 and flake8-import-order
pip install flake8
pip install flake8-import-order

# Lint
flake8 --import-order-style google
```

## Development

Build:

```bash
python3 -m pip install --upgrade build

python3 -m build
```

Upload:

```bash
python3 -m pip install --upgrade twine

twine upload dist/*
```