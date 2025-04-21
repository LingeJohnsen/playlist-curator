from dotenv import load_dotenv
from clients.curation_client import CurationClient
import os


load_dotenv()


def run():

    playlists = [
        os.getenv("DISCOVER_WEEKLY"),
        os.getenv("NEW_MUSIC_FRIDAY_CANADA"),
        os.getenv("RELEASE_RADAR"),
        os.getenv("NEW_MUSIC_FRIDAY"),
        os.getenv("NEW_MUSIC_FRIDAY_NAIJA"),
        os.getenv("NEW_MUSIC_FRIDAY_NORWAY"),
        os.getenv("NEW_MUSIC_FRIDAY_SWEDEN"),
        os.getenv("NEW_MUSIC_FRIDAY_UK"),
        os.getenv("HOT_HITS_CANADA"),
        os.getenv("NEW_MUSIC_FRIDAY_FRANCE"),
    ]

    client = CurationClient(threshold=0.7)

    results = client.curate(playlists)
    client.push_to_spotify(results)

if __name__ == "__main__":
    print("Populating Jazzy Weekly...")
    run()
    print("Done!")