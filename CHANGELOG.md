# Changelog

## 2020/11/02: `v1.0.0`

### Changes

- Deprecating support for Python < v3.6
- Upgrade SUTime to 4.0.0
- Migrate from CircleCI to Travis CI
- Migrate `setup.py` to [Poetry](https://python-poetry.org/) for package and dependency management
- Migrate to [wemake-python-styleguide](https://wemake-python-stylegui.de/)
- Fix any issues reported by `flake8`
- Add CI steps for [`safety`](https://pypi.org/project/safety/), [`bandit`](https://pypi.org/project/bandit/), and [`pyre`](https://pypi.org/project/pyre-check/), 
- Add Python type hints and type checks using [pyre](https://pyre-check.org/)
- Leverage Python 3 standard libs, such as `pathlib` and `importlib`
- Update docstrings with type hints in Google style
- Fix bugs from recent PRs
- Add Changelog and update Readme
