from msal import PublicClientApplication
import logging
import sys

def get_OAuth_token():
    app = PublicClientApplication(
        "b1d6852b-fb3f-435a-ab82-a7e5bcbe04b0",
        authority="https://login.microsoftonline.com/3f65100d-6d42-4737-8d83-3c9b1c7b56f8"
    )

    # Initialize result variable to hold the token response
    oauth_token = None

    # Check the cache to see whether we already have some accounts that the end user already used to sign in before.
    logging.info("acquiring existing accounts in cache")
    accounts = app.get_accounts()
 #   if accounts:
 #       # If so, you could then somehow display these accounts and let end user choose
 #       print("Pick the account you want to use to proceed:")
 #       for a in accounts:
 #           print(a["username"])
 #       # Assuming the end user chose this one
 #       chosen = accounts[0]
 #       # Now let's try to find a token in cache for this account
 #       oauth_token = app.acquire_token_silent(["User.Read", "Files.ReadWrite"], account=chosen)

 #   if not oauth_token:
        # So no suitable token exists in cache. Let's get a new one from Azure AD.
    logging.info("acquiring token")
    oauth_token = app.acquire_token_interactive(scopes=["User.Read", "Files.ReadWrite"])

    if "access_token" in oauth_token:
        access_token = oauth_token["access_token"]
        logging.info("Access token acquired successfully.")
        return access_token
    else:
        logging.critical("Failed to acquire access token.")
        logging.critical(oauth_token.get("error"))
        logging.critical(oauth_token.get("error_description"))
        logging.critical(oauth_token.get("correlation_id")) 
        sys.exit(1)# You may need this when reporting a bug


