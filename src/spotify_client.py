import numpy as np
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from typing import Any, Dict, List

class SpotifyClient:

    def __init__(self, client_id: str, client_secret: str, verbose: int=1):

        auth_manager = SpotifyClientCredentials(
            client_id=client_id, 
            client_secret=client_secret
        )
        self.client = spotipy.Spotify(auth_manager=auth_manager)
        self.verbose = verbose

    def get_playlist_data(self, playlist_id: str) -> List[Dict[str, Any]]:
        """Given a playlist ID get the data for each song and collect as a list 
        of dictionaries"""

        song_data = []
        next_batch = True # Dummy value to start loop
        offset = 0
        limit = 100
        batch_n = 1
        while next_batch:
            if self.verbose:
                print(f"Getting batch {batch_n} based on offset {offset} and limit {limit}...")
            batch = self.client.playlist_tracks(
                playlist_id,
                limit=limit,
                offset=offset
            )
            for i, track in enumerate(batch["items"]):
                if self.verbose: 
                    print(f"Getting track data for track {i+1}/{len(batch['items'])}...")
                self._get_track_data(track["track"], song_data)
            if batch["next"] is None:
                next_batch = False
            batch_n += 1
            offset += limit
        
        return song_data

    def _get_track_data(
        self, track: Dict[str, Any], data_list: List[Dict[str, Any]]) -> None:

        data = {}

        data["num_artists"] = len(track["artists"])
        data["duration_ms"] = track["duration_ms"]
        data["track_id"] = track["id"]
        data["track_name"] = track["name"]
        if self.verbose:
            print(f"Track name: {track['name']}")
            print("Getting audio features...")

        audio_features = self.client.audio_features(track["id"])[0]
        data["danceability"] = audio_features["danceability"]
        data["energy"] = audio_features["energy"]
        data["key"] = audio_features["key"]
        data["loudness"] = audio_features["loudness"]
        data["mode"] = audio_features["mode"]
        data["speechiness"] = audio_features["speechiness"]
        data["acousticness"] = audio_features["acousticness"]
        data["instrumentalness"] = audio_features["instrumentalness"],
        data["liveness"] = audio_features["liveness"]
        data["valence"] = audio_features["valence"]
        data["tempo"] = audio_features["tempo"]

        if self.verbose:
            print(f"Getting audio analysis data...")
        self._process_audio_analysis(track["id"], "bars", data)
        self._process_audio_analysis(track["id"], "beats", data)
        self._process_audio_analysis(track["id"], "sections", data)
        self._process_audio_analysis(track["id"], "segments", data)
        self._process_audio_analysis(track["id"], "tatums", data)

        if self.verbose:
            print("Track features gather done!")
        data_list.append(data)

    def _process_audio_analysis(self, track_id: str, feat: str, data: Dict[str, Any]) -> None:

        audio_dict = self.client.audio_analysis(track_id)

        feat_dict = audio_dict[feat]
        data[f"num_{feat}"] = len(feat_dict)

        feat_df = pd.DataFrame(feat_dict)
        
        data[f"duration_mean_{feat}"] = np.mean(feat_df["duration"])
        data[f"duration_std_{feat}"] = np.std(feat_df["duration"])




