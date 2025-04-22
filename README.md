# Playlist-curator
This playlist curator uses the Spotify API to curate Spotify generic playlists like Release Radar and New Music Friday to generate a personally tailored distilled weekly playlist. 

### Jazzy weekly

The curated playlist is called "Jazzy Weekly" - it contains tracks with a "jazzy feel" to them - often hip hop tracks with some jazz-like sound to them. Two larger playlists of 3000+ songs with either "Jazzy" or "Non-jazzy" feel to them have been created to be used as basis for the classification method used for the curation. 

### Classification

Classification is done with the help of Weaviate vector store - the basic approach is that various track features for each song in the two basis playlists are collected and stored as a single vector and stored in Weaviate with a "jazzy" property (value 0 if song is from "non-jazzy" playlist, value 1 if song is from "jazzy" playlist). New tracks are then classified by creating the same vector for each track and then do a vector search in Weaviate. If a minimum of *n* matches are found with a maximum distance of *d* then the proportion of Jazzy to Non-jazzy matches among these remaining matches is calculated and if the proportion of Jazzy matches falls above threshold *t* then the song is retained and pushed to Jazzy Weekly.

## Notes about .env vairables

Spotify client id, secret, and Spotify playlist ids necessary to load data via the Spotify API, are stored as environment variables in a .env file. These files can be obtained either from your Spotify Developer page (for client ids and secrets) or from the Spotify playlist for the playlist ids (they can be found as part of the Playlist URL).

