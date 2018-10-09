import json
import spotipy
import requests
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

#Stored variables, to change depending on user
username = 'omnitenebris'
scope = 'user-library-read'
redirectUri = 'http://www.andrewnovac.com'
clientId = '25cdc49237b348c297dff633d59bb46f'
clientSecret = 'bcef5ca156264f7085c788713e8719ec'

#Spotify Authorization 
token = util.prompt_for_user_token(username, scope,
    client_id= clientId,
    client_secret = clientSecret,
    redirect_uri = redirectUri)

#Get a list of users saved tracks
sp = spotipy.Spotify(auth=token)
results = sp.current_user_saved_tracks()

#Add the IDs of the tracks and artists
Tracks = []
Artists = []
for item in results['items']:
    track = item['track']
    Tracks.append(track['id'])
    Artists.append(track['artists'][0]['id'])

#Send out a request with the track seeds to the spotify API
seedTracks = ('%2C').join(Tracks[:5])
r = requests.get("https://api.spotify.com/v1/recommendations?market=CA&seed_tracks=" + seedTracks + "&min_energy=0.4&min_popularity=50",
    headers = {'Content-Type': 'application/json',
        'Accept': 'text/javascript',
        "Authorization": "Bearer BQC6cJ9s2jfPiQ2kAE-4I6DWdNKiKcdO7CF6REvsMnnJgn3eXiYFdhIMm8k8OSq9j2cZPwUTGO_9dv2SQU2l8U65EXVWRbZmQCLQAp7yxywTc3kJRFZ_BcX7bU41dgRawsjeree4ozT6iTAXjDDCZ96y5eNrfAtBYA"})

#Output the recommended tracks
i = 0
print("\nHere are your recommended artists: \n")
while i < 5:
    print(json.loads(r.text)['tracks'][i]['name'] + " - " +  json.loads(r.text)['tracks'][i]['artists'][0]['name'])
    i += 1
print('\n')

#Send out a request with the album seeds to the spotify API
seedArtists = ('%2C').join(Artists[:5])
r = requests.get("https://api.spotify.com/v1/recommendations?market=CA&seed_artists=" + seedArtists + "&min_energy=0.4&min_popularity=50",
    headers = {'Content-Type': 'application/json',
        'Accept': 'text/javascript',
        "Authorization": "Bearer BQA4JqQKbqrWKAwj5lOvZ-eacGQu9YY13zNE9qUHhSRCC6cesGJN60HxsscFRSwRj4npO3iBa13nMrs9FN1WxrSBpFtl4WI4iiWKXMGc2JVymhHHw9Q-ugPgNv6T5IM0TH5xnpVIKh8chI7dzHKASNP24XqSv-A"})
#print(r.text)