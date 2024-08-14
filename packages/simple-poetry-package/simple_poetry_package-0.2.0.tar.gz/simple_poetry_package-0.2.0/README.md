# Simple Poetry Package

This repository contains a minimal example of how to create, build, and deploy a Python package using [Poetry](https://python-poetry.org/). The package source code is located in the `src/simple_poetry_package` directory.

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Building the Package](#building-the-package)
- [Publishing the Package](#publishing-the-package)
- [License](#license)

## Introduction

Poetry is a tool for dependency management and packaging in Python. It allows you to manage your project’s dependencies, build your project, and publish it to PyPI or other repositories with ease. This repository provides a simple example of how to structure a Python project and use Poetry to handle its dependencies and packaging.

## Installation

To get started with this project, you'll need to have Poetry installed. If you don't have it installed yet, you can install it by following the instructions on the [official website](https://python-poetry.org/docs/#installation).

Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/rahul1990bhatia/PoetryExample.git
cd simple-poetry-package
```
Install the dependencies using Poetry:

```bash
poetry install
```

This command will create a virtual environment (if one doesn't exist) and install the dependencies specified in the pyproject.toml file.

## Project Structure

Here's an overview of the project's structure:

```
simple-poetry-package/
├── src/
│   └── simple_poetry_package/
│       ├── __init__.py
│       └── hello_world.py
│       └── cli.py
├── pyproject.toml
├── poetry.lock
└── README.md
```

- `src/simple_poetry_package/`: Contains the source code for the package.
- `pyproject.toml`: Defines the project and its dependencies.
- `poetry.lock`: Locks the project’s dependencies to specific versions.

## Building the Package

To build the package, run the following command:

```bash
poetry build
```

This command will create the distribution files (both sdist and wheel) in the dist/ directory.

## Publishing the Package

To publish the package to PyPI or another repository, you can use the following command:

```bash
poetry publish
```

Make sure you have an account on PyPI and use poetry config to set API Token.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

