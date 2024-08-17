
# DMF Utils

[![PyPI version](https://badge.fury.io/py/dmf-utils.svg)](https://pypi.org/project/dmf-utils/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dmf-utils)
[![Documentation Status](https://readthedocs.org/projects/dmf-utils/badge/?version=latest)](https://dmf-utils.readthedocs.io/en/latest/?badge=latest)
![Tests](https://github.com/memory-formation/dmf-utils/actions/workflows/tests.yml/badge.svg)
[![Project Status: WIP – Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/memory-formation/dmf-utils/blob/main/LICENSE)


DMF Utils is a Python package that provides a collection of utility functionalities to simplify common tasks in experiment and data analysis workflows. The package contains modules used by our group to facilitate tasks in neuroscience and artificial intelligence research.

## Quick Start

This package is designed in a modular way, with some functionalities included in this repository and others in separate packages that can be called from here. This allows for installing only the components needed for a specific project, aiming to maintain the broadest compatibility with different Python versions.

You can install **all modules** with pip or other package managers by running:

```bash
pip install dmf-utils[all]
```

See the [documentation](https://dmf-utils.readthedocs.io/) for more installation options and help, including how to use it in environments without internet access.

## Modules

* [Alerts](https://dmf-utils.readthedocs.io/en/latest/modules/alerts.html): Get notified when a function finishes running and send messages or files to Slack and Telegram.
* [IO (Input/Output)](https://dmf-utils.readthedocs.io/en/latest/modules/io.html): Load and save data from different formats, including CSV, Excel, and HDF5.

See the [modules documentation](https://dmf-utils.readthedocs.io/en/latest/modules/index.html) for more information.

## Documentation

For full documentation, visit [Read the Docs](https://dmf-utils.readthedocs.io/).

## Contributing

This package is maintained by [Dynamics of Memory Formation (DMF)](https://brainvitge.org/groups/memory_formation/) at the University of Barcelona. We welcome contributions from the community. If you would like to contribute, please open an issue or a pull request.

## License

DMF Utils is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
