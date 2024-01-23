# NWON Deployment

This package provides some basic functionality that we are using for our
deployment scripts and CIs.

Package is meant for internal use at [NWON](https://nwon.de) as breaking changes may occur on version changes. This may change at some point but not for now 😇.

## Working on the package

We recommend developing using poetry.

This are the steps to setup the project with a local virtual environment:

1. Tell poetry to create dependencies in a `.venv` folder withing the project: `poetry config virtualenvs.in-project true`
1. Create a virtual environment using the local python version: `poetry env use $(cat .python-version)`
1. Install dependencies: `poetry install`

## Prepare Package

Publishing the package it is not as straight forward as just calling `poetry build` 😥.

We need to:

1. Clean dist folder
1. Bump up the version of the package
1. Build the package

Luckily we provide a script for doing all of this `python scripts/prepare.py patch`. Alternatively you can run the script in a poetry context `poetry run prepare patch`. The argument at the end defines whether you want a `patch`, `minor` or `major` version bump.

The final zipped data ends up in the `dist` folder.

## Publish Package

Before publishing the package we need to:

1. Add test PyPi repository: `poetry config repositories.testpypi https://test.pypi.org/legacy/`
2. Publish the package to the test repository: `poetry publish -r testpypi`
3. Test package: `pip install --index-url https://test.pypi.org/simple/ nwon_baseline`

If everything works fine publish the package via `poetry publish`.
