# conda_export_history_versions

Tools designed for the exportation of conda environments from historical records, incorporating pinned version specifications.

## Table of Contents

- [conda\_export\_history\_versions](#conda_export_history_versions)
  - [Table of Contents](#table-of-contents)
  - [Description](#description)
  - [Installation](#installation)
  - [Usage](#usage)
  - [License](#license)

## Description

The utility `conda_export_history_versions` enables the exportation of version history for Conda environments. This functionality facilitates the tracking of temporal changes, environment reproduction, and debugging of package version-related issues.

## Installation

```bash
pip install conda_export_history_versions
```

## Usage

Help:

```bash
conda_export_history_versions -h
```

```
Export conda environment with version information.

options:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Export the modified yml into a file
  -n NAME, --name NAME  Name of the conda environment
```

Example:

```bash
conda_export_history_versions -n environment_name
```

```bash
name: environment_name
channels:
  - conda-forge
dependencies:
  - ca-certificates==2024.2.2
  - ipykernel==6.29.3
  - openssl==3.3.0
  - python=3.10
```


## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.
