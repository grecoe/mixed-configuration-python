# Mixed Configuration - Python

Some projects or test harnesses may require configuration settings to come from a wide range of sources. This project is a skeleton project to support just such a scenario by reading confirugation settings from:

- A configuration JSON file
- An INI Settings File
- The operating system environment
- Azure Key Vault

Values may be stored in different places for any number of reasons, but should be available to an application or harness via a single interface (see app.py).

## Setup

1. Create a conda environment:

> conda env create -f environment.yml

2. Run the environment:

> conda activate ConfigurationEnv

3. Find an Azure Key Vault you have access to and record the vault name and vault secret to retrieve and replace the values in the config.json file for type: "vault".

4. Ensure you are logged into Azure with the CLI

> az login

5. Run the application

> python ./app.py
