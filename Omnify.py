import math
import json
import spotipy
import requests
import spotipy.util as util
from collections import OrderedDict
from spotipy.oauth2 import SpotifyClientCredentials

#Stored variables, to change depending on user
scope = 'user-library-read user-top-read'
redirectUri = 'http://www.andrewnovac.com/journey'
clientId = '25cdc49237b348c297dff633d59bb46f'
clientSecret = 'bcef5ca156264f7085c788713e8719ec'

def main():
    #Ask for user input regarding what to do
    userRespone = input("\nType in your username: ")
    global username
    username = userRespone
    print("\nHi " + username + "!")
    artists()
    recommendations()

def artists(genres = True, artists = True, popularity = True):
    #Connect to the API
    tokenStats = util.prompt_for_user_token('omnitenebris', scope,
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
                " followers\nRanked in the " +
                ordinal(popMeter) + " percentile of artists, impressive!\n")
    
    if artists == True:
        artists = []
        for artist in json.loads(r.text)['items']:
            artists.append(artist['name'])
        print("The following are your top ten artists:")
        for i in range(0, 10):
            print("\t" + str(i + 1) + ". " + artists[i])
        print("")

    #Get users most listened to genres and return them
    if genres == True:
        print("Your favorite music falls within the following genres:")
        genres = []
        for artist in json.loads(r.text)['items']:
            genres.extend(artist['genres'])
        userGenres = ("\t- " + "\n\t- ".join(
            list
                (dict.fromkeys(
                    sorted(
                        genres,
                        key = genres.count,
                        reverse=True)
                    )
                )[:10]
            )
        )
        print(userGenres.title() + "\n")
    
    #print(r.text)

def recommendations():
    #Get the authorization
    tokenSong = util.prompt_for_user_token('omnitenebris', scope,
        client_id = clientId,
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
    print("Below are some recommended songs based on your more recent interests: \n")
    while i < 5:
        track = json.loads(r.text)['tracks'][i]['name']
        artist = json.loads(r.text)['tracks'][i]['artists'][0]['name']
        link = json.loads(r.text)['tracks'][i]['external_urls']['spotify']
        print(track + ' - ' + artist + '\n\t' + link + '\n')
        i += 1

    #Send out a request with the album seeds to the spotify API
    seedArtists = ('%2C').join(Artists[:5])
    r = requests.get("https://api.spotify.com/v1/recommendations?market=CA&seed_artists=" + seedArtists + "&min_energy=0.4&min_popularity=50",
        headers = {'Content-Type': 'application/json',
            'Accept': 'text/javascript',
            "Authorization": "Bearer " + tokenSong})

if __name__ == "__main__":
    main()