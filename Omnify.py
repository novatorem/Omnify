import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

cCManager = SpotifyClientCredentials(client_id='25cdc49237b348c297dff633d59bb46f',
                                     client_secret='bcef5ca156264f7085c788713e8719ec')
spotify = spotipy.Spotify(client_credentials_manager = cCManager)

scope = 'user-modify-playback-state'
token = util.prompt_for_user_token('omnitenebris', scope,
    client_id='25cdc49237b348c297dff633d59bb46f',
    client_secret='bcef5ca156264f7085c788713e8719ec',
    redirect_uri='http://www.andrewnovac.com')
