import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import abc

class PlaylistGenerator(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self, scope, username):
        load_dotenv()
        self.username = username
        self.token = SpotifyOAuth(scope=scope, username=username)
        self.spotifyObject = spotipy.Spotify(auth_manager=self.token)
    
    @abc.abstractmethod
    def create_playlist(self, playlist_name, playlist_description):
        self.spotifyObject.user_playlist_create(user=self.username, name=playlist_name, public=True, description=playlist_description)

    @abc.abstractmethod
    def get_tracks(self):
        pass

    @abc.abstractmethod
    def add_tracks(self, track_uris):
        prePlaylist = self.spotifyObject.user_playlists(user=self.username)
        playlist = prePlaylist['items'][0]['id']
        self.spotifyObject.user_playlist_add_tracks(user=self.username, playlist_id=playlist,tracks=track_uris)
        
    @abc.abstractmethod
    def get_link(self):
        prePlaylist = self.spotifyObject.user_playlists(user=self.username)
        playlist = prePlaylist['items'][0]['id']
        return f"https://open.spotify.com/playlist/{playlist}"
        
class PlaylistGenres(PlaylistGenerator):
    def __init__(self, scope, username):
        super().__init__(scope, username)
    
    def create_playlist(self, playlist_name, playlist_description):
        super().create_playlist(playlist_name, playlist_description)
        
    def get_tracks(self, genres, limit, country):
        # # get the genres
        # genres = self.spotifyObject.recommendation_genre_seeds()['genres']
        # print("What genres you want to include in your playlist?")
        # for i, genre in enumerate(genres):
        #     print(f"{i+1}. {genre}", end='\n')
        
        seed_genres = genres

        # get recommended tracks based off seed tracks
        recommended_tracks = self.spotifyObject.recommendations(seed_genres=seed_genres, limit=int(limit), market=country)['tracks']

        recommended_tracks_uris = [track['uri'] for track in recommended_tracks]
        return recommended_tracks_uris
    
    def get_link(self):
        return super().get_link()
        
    def add_tracks(self, track_uris):
        super().add_tracks(track_uris)
        
class PlaylistYears(PlaylistGenerator):
    def __init__(self, scope, username):
        super().__init__(scope, username)
    
    def create_playlist(self, playlist_name, playlist_description):
        super().create_playlist(playlist_name, playlist_description)
        
    def get_tracks(self, start, stop, limits, country):
        limit = int(limits)/(int(stop)-int(start))
        track_uris = []
        for year in range(int(start), int(stop)):
            results = self.spotifyObject.search(q=f'year:{year}', type='track', limit=int(limit), market=country)
            track_uris += [track['uri'] for track in results['tracks']['items']]
        return track_uris
    
    def get_link(self):
        return super().get_link()
        
    def add_tracks(self, track_uris):
        super().add_tracks(track_uris)
        
class PlaylistRecommendations(PlaylistGenerator):
    def __init__(self, scope, username):
        super().__init__(scope, username)
    
    def create_playlist(self, playlist_name, playlist_description):
        super().create_playlist(playlist_name, playlist_description)
        
    def get_tracks(self, limit, country):
        # get last played tracks
        last_played_tracks = self.spotifyObject.current_user_recently_played(limit=5)
        last_played_tracks = [track['track']['name'] for track in last_played_tracks['items']]

        seed_tracks = []
        for name in last_played_tracks:
            result = self.spotifyObject.search(q=name)
            seed_tracks.append(result['tracks']['items'][0]['uri'])

        # get recommended tracks based off seed tracks
        recommended_tracks = self.spotifyObject.recommendations(seed_tracks=seed_tracks, limit=int(limit), market=country)['tracks']

        recommended_tracks_uris = [track['uri'] for track in recommended_tracks]
        return recommended_tracks_uris
        
    def get_link(self):
        return super().get_link()
        
    def add_tracks(self, track_uris):
        super().add_tracks(track_uris)
        
        
class PlaylistAdded(PlaylistGenerator):
    def __init__(self, scope, username):
        super().__init__(scope, username)
    
    def create_playlist(self, playlist_name, playlist_description):
        super().create_playlist(playlist_name, playlist_description)
        
    def get_tracks(self):
        user_input = input("What songs do you want to add to your playlist? ")
        list_of_songs = []

        while user_input != 'quit':
            result = self.spotifyObject.search(q=user_input)
            list_of_songs.append(result['tracks']['items'][0]['uri'])
            user_input = input("What songs do you want to add to your playlist? ")
            
        return list_of_songs

    def get_link(self):
        return super().get_link()

    def add_tracks(self, track_uris):
        super().add_tracks(track_uris)
        
class PlaylistArtists(PlaylistGenerator):
    def __init__(self, scope, username):
        super().__init__(scope, username)
    
    def create_playlist(self, playlist_name, playlist_description):
        super().create_playlist(playlist_name, playlist_description)
        
    def get_tracks(self, artists, limit, country):
        list_of_artists = []
        for artist in artists:
            result = self.spotifyObject.search(q=artist, type='artist')
            list_of_artists.append(result['artists']['items'][0]['uri'])
            
        recommended_tracks = self.spotifyObject.recommendations(seed_artists=list_of_artists, limit=int(limit), market=country)['tracks']

        recommended_tracks_uris = [track['uri'] for track in recommended_tracks]
        return recommended_tracks_uris
        
    def get_link(self):
        return super().get_link()
    
    def add_tracks(self, track_uris):
        return super().add_tracks(track_uris)