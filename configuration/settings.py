import json
import os
import typing
import configparser
from abc import ABC, abstractmethod

#############################################
# Sub classes to Settings
#############################################

class IniConfiguration:
    """
    Additional settings for INI file in self.details
    """
    def __init__(self, data:dict):
        self.file:str = False
        self.section:str = None
        self.name:str = None

        for key in data:
            setattr(self, key, data[key])

class VaultConfiguration:
    """
    Additional settings for INI file in self.details
    """
    def __init__(self, data:dict):
        self.vault:str = False
        self.secret:str = None

        for key in data:
            setattr(self, key, data[key])

#############################################
# Setting and Setting types
#############################################

class Setting(ABC):
    def __init__(self):
        self.name = None
        self.type = None
        self.value = None
        self.details = None
        self.actual_value = None

    def load(self, data:dict):
        for key in data:
            setattr(self, key, data[key])

    def get(self) -> typing.Any:
        return self.actual_value

class StandardSetting(Setting):
    def __init__(self, data:dict):
        self.load(data)
        self.actual_value = self.value

class EnvironmentSetting(Setting):
    def __init__(self, data:dict):
        self.load(data)
        self.actual_value = os.environ[self.value]

class IniSetting(Setting):
    def __init__(self, data:dict):
        self.load(data)
        iconfig = IniConfiguration(self.details)

        parser = configparser.ConfigParser()
        parser.read(iconfig.file)
        self.actual_value = parser[iconfig.section][iconfig.name]

class VaultSetting(Setting):
    def __init__(self, data:dict):
        from azure.keyvault.secrets import SecretClient
        from azure.identity import DefaultAzureCredential

        self.load(data)
        vconfig = VaultConfiguration(self.details)

        client = SecretClient(
            "https://{}.vault.azure.net".format(vconfig.vault),
            DefaultAzureCredential()
        )

        self.actual_value = client.get_secret(vconfig.secret).value

