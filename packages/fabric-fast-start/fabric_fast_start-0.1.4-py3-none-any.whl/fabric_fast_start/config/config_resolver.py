import yaml
from notebookutils import mssparkutils


class ConfigResolver:
    def __init__(self, config_str):
        self.config = yaml.safe_load(config_str)
        self.resolve_config(self.config)

    def get_secret(self, akv_name, secret_name):
        return mssparkutils.credentials.getSecret(akv_name, secret_name)

    def resolve_config(self, node):
        if isinstance(node, dict):
            for key, value in node.items():
                if isinstance(value, str):
                    node[key] = self.resolve_value(value)
                else:
                    self.resolve_config(value)
        elif isinstance(node, list):
            for i, item in enumerate(node):
                if isinstance(item, str):
                    node[i] = self.resolve_value(item)
                else:
                    self.resolve_config(item)

    def resolve_value(self, value):
        # Strip surrounding quotes if present
        if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
            value = value[1:-1]

        if "{" not in value or "}" not in value:
            return value

        while "{" in value and "}" in value:
            start = value.find("{") + 1
            end = value.find("}", start)
            placeholder = value[start:end]

            if ":" not in placeholder:
                raise ValueError(f"Invalid placeholder format: {{{placeholder}}}")

            placeholder_type, placeholder_value = placeholder.split(":", 1)

            if placeholder_type == "secret":
                akv_name = self.config.get("resources", {}).get("keyvault")
                if not akv_name:
                    raise ValueError("Azure Key Vault name not found in configuration")
                replacement = self.get_secret(akv_name, placeholder_value)
            elif placeholder_type in self.config:
                if placeholder_value not in self.config[placeholder_type]:
                    raise ValueError(f"Undefined placeholder value: {placeholder_value} for type {placeholder_type}")
                replacement = self.config[placeholder_type][placeholder_value]
            else:
                raise ValueError(f"Undefined placeholder type: {placeholder_type}")

            value = value.replace("{" + placeholder + "}", str(replacement))

        return value

    def get(self, path=None):
        if path is None:
            return self.config
        keys = path.split(".")
        value = self.config
        for key in keys:
            if key in value:
                value = value[key]
            else:
                raise ValueError(f"Configuration for {path} not found")
        return value
