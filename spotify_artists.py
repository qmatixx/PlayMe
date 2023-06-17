from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
country = os.getenv("COUNTRY_CODE")

def get_token():
    auth_string = client_id + ':' + client_secret
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')
    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': 'Basic ' + auth_base64,
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {'Authorization': 'Bearer ' + token}

def search_for_artists(token, artist_name):
    url = 'https://api.spotify.com/v1/search'
    headers = get_auth_header(token)
    query = f"q={artist_name}&type=artist&limit=1"
    query_url = url + '?' + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)['artists']['items']
    if len(json_result) == 0:
        print("No artist found")
        return None
    return json_result[0]

def get_songs_by_artists(token, arists_id):
    url = 'https://api.spotify.com/v1/artists/' + arists_id + '/top-tracks?country=' + country
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)['tracks']
    return json_result
    
def get_artists_spotify():
    auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(auth_manager=auth_manager)
    featured_playlists = sp.featured_playlists(limit=50)
    artists = set()
    for playlist in featured_playlists['playlists']['items']:
        tracks = sp.playlist_tracks(playlist['id'])
        for track in tracks['items']:
            artist = track['track']['artists'][0]['name']
            artists.add(artist)
    return sorted(artists)
        
if __name__ == "__main__":
    artists = get_artists_spotify()
    for artist in artists:
        token = get_token()
        result = search_for_artists(token, artist)
        artist_id = result['id']
        songs = get_songs_by_artists(token, artist_id)
        
        # for idx, song in enumerate(songs):
        #     print(f"    {idx + 1}. {song['name']}")
                
        # print(f"{artist}: {result['genres']}")
        
        # Get artist's birthdate