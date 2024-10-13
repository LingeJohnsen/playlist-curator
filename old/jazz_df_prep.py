import feature_collection as mdat
from playlist_config import PLAYLIST_CREATOR, JAZZ_ID, NOT_JAZZ_ID
import pandas as pd

jazz_df = mdat.get_playlist_df(PLAYLIST_CREATOR, JAZZ_ID)
jazz_df['label'] = 1
other_df = mdat.get_playlist_df(PLAYLIST_CREATOR, NOT_JAZZ_ID)
other_df['label'] = 0
df = pd.concat([jazz_df, other_df])

df.to_csv('jazz.csv', sep='|')
