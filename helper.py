from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
execfile("config.py")

# Core Reporting API
def get_core_reporting_api_service():
  scope = 'https://www.googleapis.com/auth/analytics.readonly'
  key_file_location = config['client_secret_file_name']

  # Authenticate and construct service.
  service = get_service(
          api_name='analytics',
          api_version='v3',
          scopes=[scope],
          key_file_location=key_file_location)

  return service

# Common Utilits
def get_service(api_name, api_version, scopes, key_file_location):
    """Get a service that communicates to a Google API.

    Args:
        api_name: The name of the api to connect to.
        api_version: The api version to connect to.
        scopes: A list auth scopes to authorize for the application.
        key_file_location: The path to a valid service account JSON key file.

    Returns:
        A service that is connected to the specified API.
    """

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
            key_file_location, scopes=scopes)

    # Build the service object.
    service = build(api_name, api_version, credentials=credentials)

    return service

def get_the_first_profile_id(service):
    accounts = service.management().accounts().list().execute()

    if accounts.get('items'):
        account = accounts.get('items')[0].get('id')

        properties = service.management().webproperties().list(
                accountId=account).execute()

        if properties.get('items'):
            property = properties.get('items')[0].get('id')

            profiles = service.management().profiles().list(
                    accountId=account,
                    webPropertyId=property).execute()

            if profiles.get('items'):
                return profiles.get('items')[0].get('id')

    return None
