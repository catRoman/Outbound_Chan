from msal import PublicClientApplication
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.file import File
import pandas as pd
from io import BytesIO


app = PublicClientApplication(
    "b1d6852b-fb3f-435a-ab82-a7e5bcbe04b0",
    authority="https://login.microsoftonline.com/3f65100d-6d42-4737-8d83-3c9b1c7b56f8"
)

# initialize result variable to hole the token response
oauth_token = None

# We now check the cache to see
# whether we already have some accounts that the end user already used to sign in before.
accounts = app.get_accounts()
if accounts:
    # If so, you could then somehow display these accounts and let end user choose
    print("Pick the account you want to use to proceed:")
    for a in accounts:
        print(a["username"])
    # Assuming the end user chose this one
    chosen = accounts[0]
    # Now let's try to find a token in cache for this account
    oauth_token = app.acquire_token_silent(["User.Read"], account=chosen)

if not oauth_token:
    # So no suitable token exists in cache. Let's get a new one from Azure AD.
    oauth_token = app.acquire_token_interactive(scopes=["User.Read"])
if "access_token" in oauth_token:
    print(oauth_token["access_token"])  # Yay!
else:
    print(oauth_token.get("error"))
    print(oauth_token.get("error_description"))
    print(oauth_token.get("correlation_id"))  # You may need this when reporting a bug




# Define constants
site_url = 'hhttps://diamonddelivery-my.sharepoint.com/personal'
oauth_token = 'your_oauth_token'  # Replace with your actual OAuth token
file_relative_url = '/croman_rdiamondgroup_com/Documents/Sep-Obws.xlsm'  # Replace with your file path

# Create a custom AuthenticationContext to use the OAuth token
class TokenAuthenticationContext(AuthenticationContext):
    def __init__(self, site_url, token):
        super().__init__(site_url)
        self.token = token

    def acquire_token(self):
        # For OAuth token, we don't need to acquire a token, so we override this method
        return self.token

    def get_authentication_headers(self):
        # Return the headers required for authentication with the OAuth token
        return {
            'Authorization': f'Bearer {self.token}'
        }

# Initialize AuthenticationContext with OAuth token
ctx_auth = TokenAuthenticationContext(site_url, oauth_token)

# Initialize ClientContext
ctx = ClientContext(site_url, ctx_auth)

# Load the SharePoint file
response = File.open_binary(ctx, file_relative_url)

# Read the file into a Pandas DataFrame
excel_file = BytesIO(response.content)
df = pd.read_excel(excel_file, engine='openpyxl')
print(df)