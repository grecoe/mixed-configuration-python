##########################################################
# Copyright (c) Microsoft Corporation.
##########################################################
from azure.identity import ClientSecretCredential
import json
import subprocess

class CmdUtils:
    LAST_STD_ERR = None

    @staticmethod
    def get_last_errors():
        return_val = None
        if CmdUtils.LAST_STD_ERR != None:
            try:
                return_val = CmdUtils.LAST_STD_ERR.decode("utf-8")
            except UnicodeDecodeError as err:
                try:
                    return_val = CmdUtils.LAST_STD_ERR.decode("utf-16")
                except Exception as ex:
                    return_val = None
        
        CmdUtils.LAST_STD_ERR = None
        return return_val

    @staticmethod
    def get_command_output(command_list, as_json=True):
        result = subprocess.run(command_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

        CmdUtils.LAST_STD_ERR = result.stderr

        try:
            result = result.stdout.decode("utf-8")
        except UnicodeDecodeError as err:
            print("Unicode error, try again")
            print("Command was: ", " ".join(command_list))
            try:
                result = result.stdout.decode("utf-16")
            except Exception as ex:
                print("Re-attempt failed with ", str(ex))
                result = None

        if as_json and result is not None and len(result):
            return json.loads(result)

        return result

class Credential:
    """
    Get the application token using the id and secret from the 
    OSDU deployment key vault. 
    """
    def __init__(self, client, secret, tenant = None):
        self.tenant = tenant
        self.client = client
        self.secret = secret
        self.token = None

        if not self.tenant:
            result = CmdUtils.get_command_output(["az", "account", "show"])
            self.tenant = result["tenantId"]


    def get_application_token(self) -> str:
        """
        Retrieves an authentication token for the given client/secret pair
        saved in the class parameters. 

        Retrieves it only once, future calls get the same token. 
        """

        if not self.token:
            app_scope = self.client + "/.default openid profile offline_access"
        
            creds = ClientSecretCredential(
                tenant_id=self.tenant, 
                client_id=self.client, 
                client_secret=self.secret
            )
            access_token = creds.get_token(app_scope)
            self.token = access_token.token

        return self.token