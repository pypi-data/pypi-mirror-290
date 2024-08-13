[![Python Unit Tests](https://github.com/f5serge/fabric-fast-start/actions/workflows/python-tests.yaml/badge.svg)](https://github.com/f5serge/fabric-fast-start/actions/workflows/python-tests.yaml)

# Fabric Fast Start

Fabric Fast Start is a set of tools to help you get started with Fabric, including the Azure Table Configuration Manager, a Python class designed to facilitate the management of configuration data stored in Azure Table Storage. This utility allows for the storage, retrieval, and resolution of configuration settings, making it easier to manage application settings across different environments.

## Features

- Initialize with either Azure Storage Account connection string or account name and key.
- Store and retrieve configuration data by project and context.
- Resolve configurations with support for environment variable substitution.

## Requirements

- Python 3.10+
- Azure SDK for Python
- PySpark (optional)
- Delta Lake (optional)

## Installation

Ensure you have the required Azure SDK packages installed:

```bash
pip install azure-core azure-data-tables
```

## Usage

### Initialization

You can initialize the AzureTableConfigManager in one of two ways:

1. **Using an Azure Storage Account connection string:**

```python
from fabric_fast_start.config import AzureTableConfigManager

connection_string = "Your Azure Storage Account connection string"
table_name = "ConfigurationTable"
config_manager = AzureTableConfigManager(table_name, connection_string=connection_string)
```

1. **Using an Azure Storage Account name and key:**

```python
from fabric_fast_start.config import AzureTableConfigManager

account_name = "Your Azure Storage Account name"
account_key = "Your Azure Storage Account key" # pragma: allowlist secret
table_name = "ConfigurationTable"
config_manager = AzureTableConfigManager.from_account_key(account_name, account_key, table_name)
```

### Storing Configuration

To store a configuration for a specific project and context:

```python
project_name = "MyProject"
context_name = "Development"
config_str = """
resources:
  keyvault: my-keyvault
database:
  host: {DB_HOST}
  username: {secret:db-username}
  password: {secret:db-password} # pragma: allowlist secret
"""
config_manager.store_config(project_name, context_name, config_str)
```

### Retrieving and Resolving Configuration

Retrieve and resolve a configuration, optionally substituting environment variables:

```python
# Without external variables
resolved_config = config_manager.resolve_config(project_name, context_name)

# With specified environment variables
env_vars = {"DB_HOST": "localhost"}
resolved_config = config_manager.resolve_config(project_name, context_name, env_vars)

# Automatically using environment variables from os.environ
resolved_config = config_manager.resolve_config(project_name, context_name, os.environ)
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
