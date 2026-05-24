# test_token_scopes.py
import requests
from scripts.extract.auth_code_flow import get_user_token

token = get_user_token()
headers = {"Authorization": f"Bearer {token}"}

# Test /me (requires user-read-private)
resp = requests.get("https://api.spotify.com/v1/me", headers=headers)
print("/me status:", resp.status_code)

# Test /tracks
resp2 = requests.get("https://api.spotify.com/v1/tracks?ids=0WaaPFt4Qy8sVfxKz43bCD", headers=headers)
print("/tracks status:", resp2.status_code)
if resp2.status_code == 200:
    print("Success! Sample:", resp2.json()["tracks"][0]["name"])
else:
    print("Error:", resp2.text)