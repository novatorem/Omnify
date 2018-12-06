import math
import json
import spotipy
import requests
import spotipy.util as util
from collections import OrderedDict
from spotipy.oauth2 import SpotifyClientCredentials

#Stored variables, to change depending on user
username = 'omnitenebris'
scope = 'user-library-read user-top-read'
redirectUri = 'http://www.andrewnovac.com/journey'
clientId = '25cdc49237b348c297dff633d59bb46f'
clientSecret = 'bcef5ca156264f7085c788713e8719ec'

def main():
    statistics()
    songs()
"""
    #Ask for user input regarding what to do
    userRespone = input("\nType in your username: ")
    global username
    username = userRespone
    print("\nHi " + username + "! What would you like to do today?\n")
    while True:

        userRespone = input('Show my spotify statistics or recommend songs for me (stats/songs): ')
        if userRespone.lower() == "stats":
            statistics()
            break
        elif userRespone.lower() == "songs":
            songs()
            break
        else:
            print('Please type either "statistics" or "songs"\n')
"""
def songs():
    #Get the authorization
    tokenSong = util.prompt_for_user_token(username, scope,
        client_id= clientId,
        client_secret = clientSecret,
        redirect_uri = redirectUri)

    #Get a list of users saved tracks
    sp = spotipy.Spotify(auth=tokenSong)
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
            "Authorization": "Bearer " + tokenSong})

    #Output the recommended tracks
    i = 0
    print("\nHere are some recommended songs: \n")
    while i < 5:
        print(json.loads(r.text)['tracks'][i]['name'] + " - " +  json.loads(r.text)['tracks'][i]['artists'][0]['name'])
        i += 1

    #Send out a request with the album seeds to the spotify API
    seedArtists = ('%2C').join(Artists[:5])
    r = requests.get("https://api.spotify.com/v1/recommendations?market=CA&seed_artists=" + seedArtists + "&min_energy=0.4&min_popularity=50",
        headers = {'Content-Type': 'application/json',
            'Accept': 'text/javascript',
            "Authorization": "Bearer " + tokenSong})
    #print(r.text)

def statistics(genres = True, popularity = True):
    #Connect to the API
    tokenStats = util.prompt_for_user_token(username, scope,
    client_id= clientId,
    client_secret = clientSecret,
    redirect_uri = redirectUri)
    r = requests.get("https://api.spotify.com/v1/me/top/artists",
        headers = {'Content-Type': 'application/json',
            'Accept': 'text/javascript',
            "Authorization": "Bearer " + tokenStats})
    
    #Get popularity of favorite artists
    if popularity == True:
        popularity = []
        followers = []
        for artist in json.loads(r.text)['items']:
            popularity.append(artist['popularity'])
        for artist in json.loads(r.text)['items']:
            followers.append(artist['followers']['total'])
        popMeter = int(sum(popularity) / float(len(popularity)))
        folMeter = int(sum(followers) / float(len(followers)))
        ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(math.floor(n/10)%10!=1)*(n%10<4)*n%10::4])
        print("\nYour favorite artists have an average of " + str(folMeter) +
                " followers\nRanked in the top " +
                ordinal(popMeter) + " percentile of artists\n")

    #Get users most listened to genres and return them
    if genres == True:
        print("Your favorite music falls within the following genres:")
        genres = []
        for artist in json.loads(r.text)['items']:
            genres.extend(artist['genres'])
        userGenres = ("- " + "\n- ".join(
            list
                (dict.fromkeys(
                    sorted(
                        genres,
                        key = genres.count,
                        reverse=True)
                    )
                )
            )
        )
        print(userGenres.title() + "\n")
    
    #print(r.text)

if __name__ == "__main__":
    main()