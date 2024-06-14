from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import MobileApplicationClient

# Replace these with the appropriate values from your Google API Console
CLIENT_ID = 'YOUR_CLIENT_ID'
CLIENT_SECRET = 'YOUR_CLIENT_SECRET'
REDIRECT_URI = 'YOUR_REDIRECT_URI'

# Google OAuth 2.0 endpoints
AUTHORIZATION_URL = 'https://accounts.google.com/o/oauth2/v2/auth'
TOKEN_URL = 'https://www.googleapis.com/oauth2/v4/token'
USER_INFO_URL = 'https://www.googleapis.com/oauth2/v3/userinfo'

# Scopes define the level of access we are requesting.
SCOPES = ['https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile']

# OAuth2 client setup
client = MobileApplicationClient(CLIENT_ID)
oauth = OAuth2Session(client=client, redirect_uri=REDIRECT_URI, scope=SCOPES)

# The OAuth2 flow in action
def get_authorization_url():
    auth_url, state = oauth.authorization_url(AUTHORIZATION_URL, access_type="offline", prompt="select_account")
    return auth_url, state

def get_token(code):
    token = oauth.fetch_token(TOKEN_URL, client_secret=CLIENT_SECRET, code=code)
    return token

def get_user_info(token):
    oauth = OAuth2Session(CLIENT_ID, token=token)
    return oauth.get(USER_INFO_URL).json()

# Example usage
if __name__ == "__main__":
    # Step 1: Get the user to authorize and get an authorization code
    auth_url, state = get_authorization_url()
    print(f"Please go to {auth_url} and authorize access.")

    # After the user authorizes access they will be redirected to the REDIRECT_URI
    # with a code parameter which we can exchange for an access token
    authorization_response = input("Enter the full callback URL: ")
    code = oauth.parse_authorization_response(authorization_response)['code']  # Extract the code from the URL

    # Step 2: Get an access token
    token = get_token(code)
    print(f"Access token: {token}")

    # Step 3: Retrieve user info
    user_info = get_user_info(token)
    print(f"User Info: {user_info}")