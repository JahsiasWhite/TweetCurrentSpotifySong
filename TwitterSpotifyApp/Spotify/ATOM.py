#Requires spotipy to be installed
#Made by Jahsias W
import spotipy
import spotipy.util as util
from subprocess import call
import time
#Picture
from PIL import Image
import PIL
import requests
from io import BytesIO
#Help With Genius
import requests

#Your app's Client Id and Client Secret
cid = '0f4a9e39a958421b8650f7a9142baefd'
secret = 'd67ebb6b783e447c89d53175e8116752'

#Your username on Spotify
username = "Jahsias"

#Can be any url
scope = "user-read-currently-playing"
redirect_uri = "http://localhost:8888/call"

oldSong = ''
#Runs Forever...
while True:

    #Requires popup for authentication, only requires once after cached
    token = util.prompt_for_user_token(username, scope, cid, secret, redirect_uri)

    #Creates a new Spotipy object
    sp = spotipy.Spotify(auth=token)

    #Gets the current song being played and the artist
    data = sp.current_user_playing_track()
    currentSong = data['item']['name']

    #Checks if a new song is playing
    if (currentSong != oldSong):
        currentArtist = data['item']['artists'][0]['name']
        currentPicture = data['item']['album']['images'][0]['url']
        currentDemoSoundLink = data['item']['preview_url']
        currentPopularity = data['item']['popularity']
        oldSong = currentSong

        #Creates a .jpg of the current song's album picture
        response = requests.get(currentPicture)
        image = Image.open(BytesIO(response.content))
        i = image.save("spotifyPic.jpg")

        def popularity():
            if (currentPopularity >= 100):
                return("the most popular song right now")
            elif (currentPopularity >= 95):
                return("extremely popular")
            elif (currentPopularity >= 85):
                return("very popular")
            elif (currentPopularity >= 50):
                return("somewhat popular")
            elif (currentPopularity >= 25):
                return("not very popular")
            elif (currentPopularity >= 2):
                return("not popular at all")
            else:
                return("not listened to by anyone")

        #Finds how popular the song is
        result = popularity()



        #Genius API
        def request_song_info(song_title, artist_name):
            base_url = 'https://api.genius.com'
            headers = {'Authorization': 'Bearer ' + 'jpwdrAO_8VadWCwhnGdMqeDOERvKQ94QQM9oqcrkktRvNkZHPQzuPsLS2WMmPuv6'}
            search_url = base_url + '/search'
            data = {'q': song_title + ' ' + artist_name}
            response = requests.get(search_url, data=data, headers=headers)

            return response

        # Search for matches in the request response
        response = request_song_info(currentSong, currentArtist)
        json = response.json()
        remote_song_info = None

        #Finds the current song on with Genius
        for hit in json['response']['hits']:
            if currentArtist.lower() in hit['result']['primary_artist']['name'].lower():
                remote_song_info = hit
                break

        #Gets the song description
        from bs4 import BeautifulSoup
        def scrap_song_url(url):
            page = requests.get(url)
            html = BeautifulSoup(page.text, 'html.parser')
            lyrics = html.find('div', class_='rich_text_formatting').get_text()

            return lyrics

        #Checks if the song was found or not
        if remote_song_info:
            song_url = remote_song_info['result']['url']
            songDescription = scrap_song_url(song_url)
        else:
            songDescription = "Couldn't find current track on Genius"

        #Shortens description to fit 280 character limit
        currentTweetLength = len(currentSong) + len(currentArtist) +len(result) + 60
        tweetLength = 280
        charactersRemaining = tweetLength - currentTweetLength
        songDescriptionShort = songDescription[:charactersRemaining]

        #Outputs the result to a text file
        result = currentSong +" by " +currentArtist +", it's " +result +" (" +str(currentPopularity) +" percentile)\n" +songDescriptionShort +"..."
        print(len(result))
        f = open("output.txt", "w+")
        f.write(result)
        f.close()

        #Calls the .js file to tweet
        print('Calling to Twitter...')
        call(["node", "../Twitter/index.js"])

    #Waits 5 seconds before seeing if a new song is playing
    time.sleep(5)
