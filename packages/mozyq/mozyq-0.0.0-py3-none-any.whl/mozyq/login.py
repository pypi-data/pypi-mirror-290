import webbrowser

import requests
from attr import dataclass
from cattrs import structure
from fastapi import FastAPI
from google.oauth2.credentials import Credentials

CLIENT_ID = '875308481460-aoejj27l161dv2p7cohggi4iulirh9kj.apps.googleusercontent.com'
CLIENT_SECRET = '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'


@dataclass
class AuthRes:
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str
    scope: str


app = FastAPI()


webbrowser.open_new_tab(
    ''.join([
        'https://accounts.google.com/o/oauth2/v2/auth?',
        'access_type=offline&',
        'scope=https://www.googleapis.com/auth/photoslibrary.readonly&',
        'include_granted_scopes=true&',
        'prompt=consent&',
        'response_type=code&',
        'redirect_uri=http://localhost:8000/auth/&',
        f'client_id={CLIENT_ID}']))


@app.get("/auth")
async def auth(code: str):
    try:
        token_url = ''.join([
            'https://oauth2.googleapis.com/token?',
            f'client_id={CLIENT_ID}&',
            f'client_secret={CLIENT_SECRET}&',
            f'code={code}&',
            'redirect_uri=http://localhost:8000/auth/&',
            'grant_type=authorization_code'])

        res = requests.post(token_url)
        res = structure(res.json(), AuthRes)

        with open('credentials.json', 'w') as f:
            f.write(
                Credentials(
                    token=res.access_token,
                    refresh_token=res.refresh_token,
                    token_uri='https://oauth2.googleapis.com/token',
                    client_id=CLIENT_ID,
                    client_secret=CLIENT_SECRET).to_json())

        return 'ok'
    except Exception as e:
        print(e)
        return str(e)
