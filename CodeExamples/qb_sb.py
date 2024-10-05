import requests
import GetParameters as gp

client_id=gp.getParam('qb_clientId')
client_secret=gp.getParam('qb_apiSec')
sb_compId=gp.getParam('qb_sandbox_CompId')

environment='sandbox'
redirect_uri='https://developer.intuit.com/v2/OAuth2Playground/RedirectUrl'
payments_uri = 'https://sandbox.api.intuit.com/quickbooks/v4/payments'
accounting_uri = "https://sandbox-quickbooks.api.intuit.com/v3/"
from intuitlib.client import AuthClient
from intuitlib.enums import Scopes

# Set up the auth client
auth_client = AuthClient(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    environment='sandbox'  # Use 'production' for live apps
)

# Get the authorization URL
auth_url = auth_client.get_authorization_url([Scopes.ACCOUNTING])
print(f"Please visit this URL to authorize the application: {auth_url}")

# After the user grants authorization, they will be redirected to your redirect_uri
# The URL will contain a 'code' parameter. You need to extract this code.
auth_code = input("Enter the code from the redirected URL: ")

# Exchange the auth code for tokens
auth_client.get_bearer_token(auth_code)

# Now you have your tokens
print(f"Access Token: {auth_client.access_token}")
print(f"Refresh Token: {auth_client.refresh_token}")

# When the access token expires, you can use the refresh token to get a new one
auth_client.refresh()

print(f"New Access Token: {auth_client.access_token}")