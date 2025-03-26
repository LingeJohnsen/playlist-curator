from dotenv import load_dotenv
import os
from spotify_client import SpotifyClient
from typing import List

load_dotenv()

CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")

def curate(playlists: List[str]) -> None:

    raise NotImplementedError

    

