
from .settings import *

class Config:
    def __init__(self, config_json:str):
        self.settings:typing.List[Setting] = []

        loaded_settings = []
        with open(config_json, "r") as input:
            content = input.readlines()
            content = "\n".join(content)
            loaded_settings = json.loads(content)

        if len(loaded_settings):
            for data in loaded_settings:
                data_type = data["type"].lower() 
                if data_type == "json": 
                    self.settings.append(StandardSetting(data))
                elif data_type == "environ":
                    self.settings.append(EnvironmentSetting(data))
                elif data_type == "ini":
                    self.settings.append(IniSetting(data))
                elif data_type == "vault":
                    self.settings.append(VaultSetting(data))

                # Set property
                setattr(self, data["name"], self.settings[-1].get())
    
    def get(self, setting:str) -> str:
        """
        Callers retrieve the value behind a setting by passing in the setting name
        or by simply using a dot notation with the setting name as it will be loaded
        into the class instance when requested.
        """
        return_value = None
        for set in self.settings:
            if set.name.lower() == setting.lower():
                return_value = set.get()

        return return_value