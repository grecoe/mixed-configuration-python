# OSDU Simple Example with Mixed Configuration

This example shows how to use a mixed configuration and then retrieve a list of legal tags located on an OSDU instance in Azure. 

## Requirments
- OSDU Information
    - Platform and data partition names of the OSDU instance
    - If OSDU is not on Azure then modify the URI's in the platform.ini
- Azure Key Vault 
    - Containes two secrets that identify an Azure Service Principal
    - Logged in user of Azure CLI has access to read secrets from the key vault. 

## Usage

The application will take the platform and partition name from the config.json file. The platform legal tags URI from the platform.ini, and service principal information from the key vault contained within Azure. 

Using this configuration information, the application will retrieve all of the legal tags from the OSDU system. 

> <b>NOTE</b> This approach is ONLY using a service princpal, which is not recommended for anything other than testing. Any actual work to be done with OSDU should be using user credentials to ensure that the application does NOT access information that the operator is not privy to. 