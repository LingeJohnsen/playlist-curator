from utils.dataset_generation import create_vector_data
from dotenv import load_dotenv
import os
from clients.spotify_client import SpotifyClient
from typing import Dict, List, Tuple
import weaviate
from weaviate.classes.query import MetadataQuery
from clients.weaviate_client import WeaviateClient


load_dotenv()


class CurationClient:

    def __init__(self, match_limit=20, threshold=0.5, verbose=0):

        self.wviate = WeaviateClient()
        self.spotify = SpotifyClient()
        self.match_limit = match_limit
        self.threshold = threshold
        self.verbose = verbose


    def curate(self, playlists: List[str] | str) -> None:

        if isinstance(playlists, str):
            playlists = [playlists]
        jazzy = []
        for i, playlist in enumerate(playlists):
            print(f"Processing playlist {i+1}/{len(playlists)}")
            matches = self.get_playlist_matches(playlist)
            results = self.process_matches_all(matches)
            jazzy.extend(results)
        self.wviate.client.close()
        return jazzy


    def get_playlist_matches(self, playlist: str) -> List[Tuple[str, List[weaviate.collections.classes.internal.Object]]]:

        tracks = self.wviate.client.collections.get("tracks")
        vector_data = create_vector_data(playlist, verbose=self.verbose)
        matches = []
        for vec in vector_data:
            response = tracks.query.near_vector(
                near_vector=vec["vector"],
                limit=self.match_limit,
                return_metadata=MetadataQuery(distance=True)
            )
            matches.append((vec["id"], response.objects))
        return matches
    
    def process_matches_all(self, matches: List[Tuple[str, List[weaviate.collections.classes.internal.Object]]]) -> List[str]:
        """Go through each matches for all songs in a list and filter out tracks 
        where the proportion of matches to Jazzy to non-Jazzy fall below the 
        threshold"""

        res = []
        for match in matches:
            if self.verbose > 0:
                print(f"Processing {match[0]}...")
            prop = self.process_matches(match)
            if self.verbose > 0:
                print(f"Match prop: {prop}")
            # Filter out songs with below threshold matches
            if prop[match[0]] >= self.threshold:
                if self.verbose > 0:
                    print(f"Including {match[0]}...")
                res.append(prop)
        return res

    def process_matches(self, matches: Tuple[str, List[weaviate.collections.classes.internal.Object]]) -> Dict[str, float]:

        id = matches[0]
        query_res = matches[1]
        jazzy_count = 0
        for res in query_res:
            jazzy_count += res.properties["jazzy"]
        jazzy_proportion = jazzy_count/self.match_limit
        return {id: jazzy_proportion}
    
    def push_to_spotify(self, tracks: List[Dict[str, float]]):

        ids = list(set([list(t.keys())[0] for t in tracks]))

        self.spotify.client.playlist_replace_items(os.getenv("JAZZY_WEEKLY"), ids)






