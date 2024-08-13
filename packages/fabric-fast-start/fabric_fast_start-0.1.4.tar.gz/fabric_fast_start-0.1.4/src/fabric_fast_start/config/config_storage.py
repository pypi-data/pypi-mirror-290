import os

from azure.core.credentials import AzureNamedKeyCredential
from azure.core.exceptions import ResourceExistsError
from azure.data.tables import TableServiceClient

from .config_resolver import ConfigResolver


class AzureTableConfigManager:
    # can initialize the class with a connection string and table name
    # or with storage account name and key and table name
    def __init__(self, table_name, account_name=None, account_key=None, connection_string=None):
        self.table_name = table_name
        self.account_name = account_name
        self.account_key = account_key
        self.connection_string = connection_string
        self.table_client = self._get_table_client()

    @classmethod
    def from_account_key(cls, account_name, account_key, table_name):
        return cls(table_name, account_name=account_name, account_key=account_key)

    @classmethod
    def from_connection_string(cls, connection_string, table_name):
        return cls(table_name, connection_string=connection_string)

    # def __init__(self, connection_string, table_name):
    #     self.connection_string = connection_string
    #     self.table_name = table_name
    #     self.table_client = self._get_table_client()

    def _get_table_client(self):
        if self.account_name and self.account_key:
            endpoint_url = f"https://{self.account_name}.table.core.windows.net/"
            credential = AzureNamedKeyCredential(self.account_name, self.account_key)
            table_service_client = TableServiceClient(endpoint=endpoint_url, credential=credential)
        else:
            table_service_client = TableServiceClient.from_connection_string(self.connection_string)
        try:
            table_service_client.create_table(self.table_name)
        except ResourceExistsError:
            pass
        return table_service_client.get_table_client(self.table_name)

    def store_config(self, project_name, context_name, config_str):
        entity = {"PartitionKey": project_name, "RowKey": context_name, "ConfigData": config_str}
        self.table_client.upsert_entity(entity)

    def retrieve_config(self, project_name, context_name):
        try:
            entity = self.table_client.get_entity(project_name, context_name)
            return entity["ConfigData"]
        except Exception:
            return None

    def resolve_config(self, project_name, context_name, env_vars=None):
        config_str = self.retrieve_config(project_name, context_name)
        if config_str:
            resolver = ConfigResolver(config_str)

            # Use provided env_vars or get from os.environ if not provided
            if env_vars is None:
                env_vars = dict(os.environ)

            # Update the config with environment variables
            for key, value in env_vars.items():
                resolver.config[key] = value

            return resolver
        else:
            raise ValueError(f"Configuration for project '{project_name}' and context '{context_name}' not found")


# # Updated Usage example:
# # Initialize the AzureTableConfigManager with a connection string and table name
# connection_string = "Your Azure Storage Account connection string"
# table_name = "ConfigurationTable"
# config_manager = AzureTableConfigManager(connection_string, table_name)

# Or initialize with storage account name and key
# account_name = "Your Azure Storage Account name"
# account_key = "Your Azure Storage Account key" # pragma: allowlist secret
# table_name = "ConfigurationTable"
# config_manager = AzureTableConfigManager.from_account_key(account_name, account_key, table_name)


# # Storing a configuration for a project in a specific context
# project_name = "MyProject"
# context_name = "Development"
# config_str = """
# resources:
#   keyvault: my-keyvault
# database:
#   host: {DB_HOST}
#   username: {secret:db-username}
#   password: {secret:db-password}
# """
# config_manager.store_config(project_name, context_name, config_str)

# # Retrieving and resolving a configuration without external variables
# resolved_config = config_manager.resolve_config(project_name, context_name)
# db_host = resolved_config.get("database.host")
# db_username = resolved_config.get("database.username")
# db_password = resolved_config.get("database.password")

# # Retrieving and resolving a configuration with specified environment variables
# env_vars = {"DB_HOST": "localhost"}
# resolved_config = config_manager.resolve_config(project_name, context_name, env_vars)
# db_host = resolved_config.get("database.host", env_vars)
# db_username = resolved_config.get("database.username", env_vars)
# db_password = resolved_config.get("database.password", env_vars)

# # Retrieving and resolving a configuration, automatically using environment variables from os.environ
# resolved_config = config_manager.resolve_config(project_name, context_name, os.environ)
# db_host = resolved_config.get("database.host")
# db_username = resolved_config.get("database.username")
# db_password = resolved_config.get("database.password")
