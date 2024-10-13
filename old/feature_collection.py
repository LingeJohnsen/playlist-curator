import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from config import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET
import numpy as np
import pandas as pd

def authenticate():
    token = SpotifyClientCredentials(
                                     client_id=SPOTIPY_CLIENT_ID, 
                                     client_secret=SPOTIPY_CLIENT_SECRET
                                    )
    cache_token = token.get_access_token()
    sp = spotipy.Spotify(cache_token)
    return sp

def get_playlist_df(creator_name, playlist_id):
    '''Combines metadata and track features into one df.
    
    Args: 
    creator_name(str): User name for creator of playlist.
    playlist_id(str): Playlist id.
    
    Returns:
    df(pd.DataFrame): DataFrame with metadata (track id, name, artist(s)
    etc., and audio features.)
    '''
    
    meta_dict = get_features(creator_name, playlist_id)
    # Remove NoneType items in features 
    features_dict = []
    for f_dict in meta_dict['features']:
        if f_dict:
            features = {k: v for k, v in f_dict.items()}
            features_dict.append(features)
       
    
    # Features collected twice and that should be removed from one dataset
    drop_cols = [
                 'key',
                 'loudness', 
                 'mode', 
                 'tempo', 
                 'duration_ms', 
                 'time_signature'
                ]

    base_keys = ['track_id', 'song_name', 'artist', 'album']
    base_dict = {key: meta_dict.get(key) for key in base_keys}
    base_df = pd.DataFrame.from_dict(base_dict).set_index('track_id')

    features_df = pd.DataFrame.from_dict(features_dict)\
                    .rename(columns={'id': 'track_id'})\
                    .drop(drop_cols, axis=1)\
                    .set_index('track_id')
                    
    analysis_tracks = []
    for a_dict in meta_dict['analysis_features']:
        if a_dict:
            a_features = {k: v for k, v in a_dict.items()}
            analysis_tracks.append(a_features)
    analysis_df = get_analysis_df(analysis_tracks).set_index('track_id')

    df = base_df.join(features_df).join(analysis_df)
    
    return df

def get_artist_df(artist_id):
    '''Combines metadata and track features into one df.
    
    Args: 
    artist_id(str): Artist id.
    
    Returns:
    df(pd.DataFrame): DataFrame with metadata (track id, name, artist(s)
    etc., and audio features.)
    '''
    
    meta_dict = get_features(artist_id=artist_id)
    # Remove NoneType items in features 
    features_dict = []
    for f_dict in meta_dict['features']:
        if f_dict:
            features = {k: v for k, v in f_dict.items()}
            features_dict.append(features)
       
    
    # Features collected twice and that should be removed from one dataset
    drop_cols = [
                 'key',
                 'loudness', 
                 'mode', 
                 'tempo', 
                 'duration_ms', 
                 'time_signature'
                ]

    base_keys = ['track_id', 'song_name', 'artist', 'album']
    base_dict = {key: meta_dict.get(key) for key in base_keys}
    base_df = pd.DataFrame.from_dict(base_dict).set_index('track_id')

    features_df = pd.DataFrame.from_dict(features_dict)\
                    .rename(columns={'id': 'track_id'})\
                    .drop(drop_cols, axis=1)\
                    .set_index('track_id')
                    
    analysis_tracks = []
    for a_dict in meta_dict['analysis_features']:
        if a_dict:
            a_features = {k: v for k, v in a_dict.items()}
            analysis_tracks.append(a_features)
    analysis_df = get_analysis_df(analysis_tracks).set_index('track_id')

    df = base_df.join(features_df).join(analysis_df)
    
    return df
    

def get_features(creator_name=None, playlist_id=None, artist_id=None):
    '''Gets a dictionary with all metadata for the tracks in the playlist or 
    for a specified artist.
    
    Args: 
    creator_name(str): User name for creator of playlist.
    playlist_id(str): Playlist id.
    artist_id(str): Artist id.
    
    Returns:
    meta_dict(dictionary): dictionary with metadata
    '''
    
    def _get_track_features_playlist(track_item, sp):
        
        print('Loading new item number {}...'.format(len(track_id_list)+1))
        try:
            track_id = track_item['track']['id']
            track_id_list.append(track_id)
            
            song_name = track_item['track']['name']
            song_name_list.append(song_name)
                    
            song_artists = ''
            artist_num = len(track_item['track']['artists'])
            artist_index = 0
            for artist in track_item['track']['artists']:
                artist_index += 1
                if artist_index == artist_num:
                    song_artists += artist['name']
                else:
                    song_artists += artist['name'] + ', '
            # song_artists = song_artists.rstrip(', ')
            artist_list.append(song_artists)
        
            album_name = track_item['track']['album']['name']
            album_list.append(album_name)
            
            track_features = sp.audio_features(track_id)[0]
            features_list.append(track_features)
                    
            track_analysis = sp.audio_analysis(track_id)
            track_analysis['track_id'] = track_id
            analysis_list.append(track_analysis)
            
            print('Loaded item {} - {}'.format(song_name, album_name))
        except:
            print(
                  'Failed to load track {}. Moving on to next song.'
                  .format(len(track_id_list)+1)
                 )
    
    def _get_features_playlist(creator_name, playlist_id):
        
        songs_missing = True
        sp = authenticate()
        offset = 0
        
        while songs_missing is True:
            # Re-authenticate if lose authentication during run
            try:
                playlist_dict = sp.user_playlist_tracks(
                                                        creator_name, 
                                                        playlist_id,
                                                        limit=100,
                                                        offset=offset
                                                       )
            except spotipy.client.SpotifyException:
                sp = authenticate()
                playlist_dict = sp.user_playlist_tracks(
                                                        creator_name, 
                                                        playlist_id,
                                                        limit=100,
                                                        offset=offset
                                                       )
        
            for item in playlist_dict['items']: 
                
                _get_track_features_playlist(item, sp)
                
            offset += 100
              
            if playlist_dict['next'] is None:
                songs_missing = False
                print('Finished loading metadata.')
            else:
                songs_missing = True
                
    def _get_track_features_artist(track_item, sp):
        print('Loading new item number {}...'.format(len(track_id_list)+1))
        try:
            track_id = track_item['id']
            track_id_list.append(track_id)
            
            song_name = track_item['name']
            song_name_list.append(song_name)
                    
            song_artists = ''
            artist_num = len(track_item['artists'])
            artist_index = 0
            for artist in track_item['artists']:
                artist_index += 1
                if artist_index == artist_num:
                    song_artists += artist['name']
                else:
                    song_artists += artist['name'] + ', '
            # song_artists = song_artists.rstrip(', ')
            artist_list.append(song_artists)
            
            track_features = sp.audio_features(track_id)[0]
            features_list.append(track_features)
                    
            track_analysis = sp.audio_analysis(track_id)
            track_analysis['track_id'] = track_id
            analysis_list.append(track_analysis)
            
            print('Loaded item {}'.format(song_name))
        except:
            print(
                  'Failed to load track {}. Moving on to next song.'
                  .format(len(track_id_list)+1)
                 )
    
    def _get_features_artist(artist_id):
        
        def _build_album_dict(album_dict):
            
            for item in album_dict['items']:
                albums[item['id']] = item['name']
            
                
        sp = authenticate()
                
        albums = {}
        
        # First get the albums of an artist
        albums_artist = sp.artist_albums(artist_id, album_type = 'album')
        _build_album_dict(albums_artist)            
        singles_artist = sp.artist_albums(artist_id, album_type = 'single')
        _build_album_dict(singles_artist)  
        compilations_artist = sp.artist_albums(artist_id, album_type = 'compilation')
        _build_album_dict(compilations_artist)  
        appear_artist = sp.artist_albums(artist_id, album_type = 'appears_on')
        _build_album_dict(appear_artist)
        
        for aid, album_name in albums.items():
            album_tracks = sp.album_tracks(aid)
            for track in album_tracks['items']:
                album_list.append(album_name)
                _get_track_features_artist(track, sp)     
    
    track_id_list = []
    song_name_list  = []
    artist_list  = []
    album_list  = []
    features_list = []
    analysis_list = []
    
    if creator_name and playlist_id:
        _get_features_playlist(creator_name, playlist_id)
    elif artist_id:
        _get_features_artist(artist_id)    
    
    meta_dict = {
                 'track_id': track_id_list,
                 'song_name': song_name_list,
                 'artist': artist_list,
                 'album': album_list,
                 'features': features_list,
                 'analysis_features': analysis_list
                }
    
    return meta_dict
    
def get_analysis_df(analysis_tracks):
    '''Gather dictionary with audio analysis features into a dataframe
    
    Args:
    analysis_tracks(dict): dictionary with audio analysis features.
    
    Returns:
    df(DataFrame): dataframe with collected and aggregated data.
    '''
    
    for i, track in enumerate(analysis_tracks):
        track_df = pd.DataFrame(track['track'], index=[i])
        bars = pd.DataFrame(track['bars'])
        track_df['bars_num'] = len(bars)
        try:
            track_df['bars_duration_mean'] = np.mean(bars['duration'])
            track_df['bars_duration_var'] = np.std(bars['duration'])
        except: 
            track_df['bars_duration_mean'] = None
            track_df['bars_duration_var'] = None
        beats = pd.DataFrame(track['beats'])
        track_df['beats_num'] = len(beats)
        try:
            track_df['beats_duration_mean'] = np.mean(beats['duration'])
            track_df['beats_duration_var'] = np.std(beats['duration'])
        except:
            track_df['beats_duration_mean'] = None
            track_df['beats_duration_var'] = None
        sections = pd.DataFrame(track['sections'])
        track_df['sections_num'] = len(sections)
        try:
            track_df['sections_duration_mean'] = np.mean(sections['duration'])
            track_df['sections_duration_var'] = np.std(sections['duration'])
        except:
            track_df['sections_duration_mean'] = None
            track_df['sections_duration_var'] = None
        try:
            track_df['loudness_var'] = np.std(sections['loudness'])
        except:
            track_df['loudness_var'] = None
        try:
            track_df['tempo_var'] = np.std(sections['tempo'])
        except:
            track_df['tempo_var'] = None
        try:
            track_df['key_var'] = np.std(sections['key'])
        except:
            track_df['key_var'] = None
        try:
            track_df['mode_var'] = np.std(sections['mode'])
        except:
            track_df['mode_var'] = None
        segments = pd.DataFrame(track['segments'])
        track_df['segments_num'] = len(segments)
        try:
            track_df['segments_duration_mean'] = np.mean(segments['duration'])
            track_df['segments_duration_var'] = np.std(segments['duration'])
        except:
            track_df['segments_duration_mean'] = None
            track_df['segments_duration_var'] = None
        try:
            mean_pitches = pd.DataFrame(segments['pitches'].values.tolist()).mean(1)
            track_df['pitches_mean'] = np.mean(mean_pitches)
            track_df['pitches_var'] = np.std(mean_pitches)
        except:
            track_df['pitches_mean'] = None
            track_df['pitches_var'] = None
        try:
            mean_timbre = pd.DataFrame(segments['timbre'].values.tolist()).mean(1)
            track_df['timbre_mean'] = np.mean(mean_timbre)
            track_df['timbre_var'] = np.std(mean_timbre)
        except:
            track_df['timbre_mean'] = None
            track_df['timbre_var'] = None
        tatums = pd.DataFrame(track['tatums'])
        track_df['tatums_num'] = len(tatums)
        try:
            track_df['tatums_duration_mean'] = np.mean(tatums['duration'])
            track_df['tatums_duration_var'] = np.std(tatums['duration'])
        except:
            track_df['tatums_duration_mean'] = None
            track_df['tatums_duration_var'] = None
        track_df['track_id'] = track['track_id']
        if i > 0:
            df = pd.concat([df, track_df])
        else:
            df = track_df.copy()
    return df