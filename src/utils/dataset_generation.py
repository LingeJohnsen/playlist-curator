from clients.spotify_client import SpotifyClient
from typing import Any, Dict, List

def create_vector_data(playlist_id: str, verbose: int=0) -> List[Dict[str, Any]]:

    spotify = SpotifyClient(verbose=verbose)

    dataset = spotify.get_playlist_data(playlist_id)
    vector_dataset = []

    for data in dataset:
        vector = [
            float(data["danceability"]),
            float(data["energy"]),
            float(data["key"]),
            float(data["loudness"]),
            float(data["mode"]),
            float(data["speechiness"]), 
            float(data["acousticness"]),
            float(data["instrumentalness"][0]), # For some reason this is a tuple with one element
            float(data["liveness"]),
            float(data["valence"]),
            float(data["tempo"]),
            float(data["num_bars"]),
            float(data["duration_mean_bars"]),
            float(data["duration_std_bars"]),
            float(data["num_beats"]),
            float(data["duration_mean_beats"]),
            float(data["duration_std_beats"]),
            float(data["num_sections"]),
            float(data["duration_mean_sections"]),
            float(data["duration_std_sections"]),
            float(data["num_segments"]),
            float(data["duration_mean_segments"]),
            float(data["duration_std_segments"]),
            float(data["num_tatums"]),
            float(data["duration_mean_tatums"]),
            float(data["duration_std_tatums"]),
        ]
        vector_dict = {
            "id": data["track_id"],
            "title": data["track_name"],
            "vector": vector
        }
        vector_dataset.append(vector_dict)

    return vector_dataset


def create_dataset(ids: List[str]) -> List[Dict[str, Any]]:

    dataset = []
    
    for id in ids:
        print(f"Creating vector data from id {id}...")
        dataset.extend(create_vector_data(id))
    print("Dataset generation done!")

    return dataset