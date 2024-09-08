import msal
import logging
import sys
import tkinter as tk
from tkinterweb import HtmlFrame
import json
import time
import queue


logging = logging.getLogger(__name__)

def get_OAuth_token():
    app = msal.PublicClientApplication(
        "b1d6852b-fb3f-435a-ab82-a7e5bcbe04b0",
        authority="https://login.microsoftonline.com/3f65100d-6d42-4737-8d83-3c9b1c7b56f8"
    )

    # Initialize result variable to hold the token response
    oauth_token = None

    # Check the cache to see whether we already have some accounts that the end user already used to sign in before.
    logging.info("acquiring existing accounts in cache")
   

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
        sys.exit(1)


