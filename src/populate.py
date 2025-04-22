from utils.dataset_generation import create_dataset
from dotenv import load_dotenv
import os
from typing import List
from clients.weaviate_client import WeaviateClient

load_dotenv()

CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
PLAYLISTS = [
    os.getenv("JAZZ_ID"),
    os.getenv("NOT_JAZZ_ID")
]

def populate(playlist: List[str] | str, jazzy: bool) -> None:

    if not isinstance(playlist, list):
        playlist = [playlist]

    dataset = create_dataset(playlist)

    weaviate_client = WeaviateClient()

    if not weaviate_client.client.collections.exists("tracks"):
        weaviate_client.create_collection("tracks", vector_name="spotify_tracks")
    
    weaviate_client.populate_collection("tracks", jazzy, dataset)


if __name__ == "__main__":
    print(f"Start populating Weaviate with data from playlists {PLAYLISTS}...")
    for playlist in PLAYLISTS:
        if playlist == os.getenv("JAZZ_ID"):
            print("Populating jazzy dataset...")
            populate(playlist, jazzy=True)
        elif playlist == os.getenv("NOT_JAZZ_ID"):
            print("Populating non-jazzy dataset...")
            populate(playlist, jazzy=False)
    print("Population done!")