from dataset_generation import create_dataset
from dotenv import load_dotenv
import os
from typing import List
from weaviate_client import WeaviateClient

load_dotenv()

CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
PLAYLISTS = [
    os.getenv("JAZZ_ID"),
    os.getenv("NOT_JAZZ_ID")
]

def populate(playlists: List[str]) -> None:

    dataset = create_dataset(playlists)

    weaviate_client = WeaviateClient("./vector_store/")

    if not weaviate_client.client.collections.exists("tracks"):
        weaviate_client.create_collection("tracks")
    
    weaviate_client.populate_collection("tracks", dataset)


if __name__ == "__main__":
    print(f"Start populating Weaviate with data from playlists {PLAYLISTS}...")
    populate(PLAYLISTS)
    print("Population done!")