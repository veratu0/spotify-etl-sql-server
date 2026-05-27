import os
from dotenv import load_dotenv
from requests_oauthlib import OAuth2Session
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import threading
import time

load_dotenv()

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = "http://127.0.0.1:8080"
# Required to read private playlists
SCOPE = "playlist-read-private user-read-private"

# HTTP server to catch the redirect and get the authorization code
auth_code = None
class CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global auth_code
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)
        if 'code' in params:
            auth_code = params['code'][0]
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Authorization successful! You can close this window.")
        else:
            self.send_response(400)
            self.end_headers()

def get_user_token():
    global auth_code
    spotify = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, scope=SCOPE)
    authorization_url, state = spotify.authorization_url('https://accounts.spotify.com/authorize')
    webbrowser.open(authorization_url)

    # Start a local server to listen for the callback
    with HTTPServer(('127.0.0.1', 8080), CallbackHandler) as httpd:
        # Server will run in a separate thread to not block the main script
        server_thread = threading.Thread(target=httpd.handle_request)
        server_thread.start()
        # Wait for the auth_code to be set by the server
        while auth_code is None:
            time.sleep(1)

    # Exchange the authorization code for an access token
    token_url = 'https://accounts.spotify.com/api/token'
    token = spotify.fetch_token(
        token_url,
        code=auth_code,
        client_secret=CLIENT_SECRET,
        include_client_id=True
    )
    return token['access_token']

if __name__ == '__main__':
    token = get_user_token()
    print("User-specific token obtained:", token[:50], "...")
