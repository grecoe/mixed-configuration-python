import os
from configuration.config import Config

# Create environment variable to load, as noted in config.json
os.environ["ENV_VAR_1"] = "From os.environ"

# Contains a definition of all settings to be loaded.
conf = Config("./config.json")


"""
Simply ask the config for a setting and it will be retrieved from wherever
it lives based on the configuration. 

Note that all settings are also properties of the Config class itself and can
be called with dot notation directly. 
"""

# In json
print("JSON   :", conf.get("JsonSetting"), " : ", conf.JsonSetting)
# In os.environ
print("ENVIRON:",conf.get("EnvSetting"))
# In ini
print("INI    :",conf.get("IniSetting"))
# Key Vault
print("VAULT  :",conf.get("VaultSetting"))