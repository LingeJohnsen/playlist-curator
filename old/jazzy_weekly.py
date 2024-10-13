import feature_collection as mdat
from playlist_config import PLAYLIST_CREATOR
import playlist_config as pc
from config import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET
import tensorflow.keras as tfk
from joblib import load
import pandas as pd
import spotipy
import spotipy.util as util

# Load model
jazzy_model = tfk.models.load_model('jazz_model')

# Load weekly playlists
weekly_df = mdat.get_playlist_df(PLAYLIST_CREATOR, pc.DISCOVER_WEEKLY)
new_df = mdat.get_playlist_df(PLAYLIST_CREATOR, pc.NEW_MUSIC_FRIDAY)
release_df = mdat.get_playlist_df(PLAYLIST_CREATOR, pc.RELEASE_RADAR)
new_canada_df = mdat.get_playlist_df(PLAYLIST_CREATOR, pc.NEW_MUSIC_FRIDAY_CANADA)
new_naija_df = mdat.get_playlist_df(PLAYLIST_CREATOR, pc.NEW_MUSIC_FRIDAY_NAIJA)
new_norway_df = mdat.get_playlist_df(PLAYLIST_CREATOR, pc.NEW_MUSIC_FRIDAY_NORWAY)
new_sweden_df = mdat.get_playlist_df(PLAYLIST_CREATOR, pc.NEW_MUSIC_FRIDAY_SWEDEN) 
new_uk_df = mdat.get_playlist_df(PLAYLIST_CREATOR, pc.NEW_MUSIC_FRIDAY_UK) 
new_france_df = mdat.get_playlist_df(PLAYLIST_CREATOR, pc.NEW_MUSIC_FRIDAY_FRANCE)

df_list = [
            weekly_df, 
            new_df, 
            release_df, 
            new_canada_df,
            new_naija_df, 
            new_norway_df,
            new_sweden_df,
            new_uk_df,
            new_france_df
          ]

features = [
            'danceability',
            'energy',
            'speechiness',
            'acousticness',
            'instrumentalness',
            'liveness',
            'valence',
            'num_samples',
            'end_of_fade_in',
            'loudness',
            'tempo',
            'key',
            'mode',
            'bars_num',
            'bars_duration_var',
            'beats_duration_var',
            'sections_num',
            'sections_duration_mean',
            'sections_duration_var',
            'loudness_var',
            'tempo_var',
            'key_var',
            'mode_var',
            'segments_duration_var',
            'segments_duration_mean',
            'pitches_mean',
            'pitches_var',
            'timbre_mean',
            'timbre_var',
            'tatums_duration_var'
            ]
concats = pd.concat(df_list, axis=0)
concats.drop_duplicates(inplace=True)
songs = concats.copy()
X = concats[features].copy()
del concats

# Find the jazzy songs - first have to scale model as in trained dataset
scaler = load('scaler.joblib')
X_scaled = scaler.transform(X)
del X

# Find songs to try out
songs['scores'] = jazzy_model.predict(X_scaled)
songs['predictions'] = songs['scores'].round(0)
songs = songs[songs['predictions']==1]
songs = songs[['song_name', 'artist', 'album', 'scores', 'predictions']]
song_ids = songs.index.tolist()

# Add songs to playlist
token = util.prompt_for_user_token(
                                   PLAYLIST_CREATOR,
                                   scope = 'playlist-modify-public',
                                   client_id = SPOTIPY_CLIENT_ID, 
                                   client_secret = SPOTIPY_CLIENT_SECRET,
                                   redirect_uri = 'http://localhost:8888/callback'
                                  )
sp = spotipy.Spotify(token)
sp.user_playlist_replace_tracks(PLAYLIST_CREATOR, pc.JAZZY_WEEKLY, song_ids)