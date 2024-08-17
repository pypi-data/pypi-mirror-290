import json
import string
import webbrowser
from random import choices

from attr import dataclass
from websockets.client import connect


@dataclass
class AuthRes:
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str
    scope: str


async def login():
    state = ''.join(choices(string.ascii_letters, k=10))

    async with connect("wss://api.mozyq.org/ws") as websocket:
        await websocket.send(state)
        url = f'https://api.mozyq.org/login?state={state}'
        print('Login URL:')
        print(url)
        webbrowser.open_new_tab(url)

        auth = await websocket.recv()
        auth = json.loads(auth)

        with open('credentials.json', 'w') as f:
            json.dump(auth, f)
