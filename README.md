# ais-dev2il-mlops-taxi-rides


## Setup

```
# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate

# Install runtime requirements and add project in edit mode
pip install -e .
# Install development and test requirements
pip install .[dev]
pip install .[test]
```

## Notebook environment

Run `jupyter notebook` to work with the notebooks without IDE.

When using an IDE, make sure that the IDE is configured to use the project's virtual environment and that that the notebook working directory is the directory where the notebook files is located.

## Testing 

Run `pytest`.
In order to see logging and stdout outputs, use `pytest -s --log-cli-level=DEBUG`.

## Working with Docker on your developer machine

To build the `taxi-rides-outlier-detection` image, run `sh build-image.sh`. 

To find outliers from a file on your local file system run `sh run-container.sh`

## Working With the GitHub Packages Container Registry

### Using the Terminal 

In order to authenticate, you need to create a personal access token and authenticate. Follow the steps as outlined here: https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry#authenticating-with-a-personal-access-token-classic

To build the `taxi-rides-outlier-detection` image, run `sh build-image-gitlab.sh`. 

To find outliers from a file on your local file system run `sh run-container-gitlab.sh`

### Using GitHub Actions

See https://docs.github.com/en/actions/use-cases-and-examples/publishing-packages/publishing-docker-images#publishing-images-to-github-packages


## xxx


https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page
https://www.kaggle.com/datasets/elemento/nyc-yellow-taxi-trip-data


Parquet
Visual Studio Code: Parquet Visualizer


1. Setup pyproject.toml (minimal, we'll extend it while creating the notebook)
1. Copy the notebook
1. Download the data
1. Analyse the data. Explain simple SQL with Parquet Visualizer Extension
1. Compare the file sizes (csv kaggle, parquet)
1. Walk through the notebook and setup the dependencies (dev deps, runtime deps)
1. Setup the python module. Also include it in pyproject.toml. Install the source once available (pip ... -e)
1. Create the outlier detection function (empty)
1. Create the test fixture
1. Create the test
1. TDD until test runs (pytest -s)
1. Copy over the code from the notebook 
1. Make the test green with real life code
1. Switch to logging (pytest -s --log-cli-level=DEBUG)
1. Create the CLI script. TODO log files, etc. ?
1. Explain the click library
1. Create the Dockerfile, build it and run it on the local system
1. Copy the GitHub Workflow and let it build remotely
1. Run the Dockerfile using the remote image


? static code analysis - take over from Johannes ? 
? security vulnerability scanning - take over from Johannes ? 