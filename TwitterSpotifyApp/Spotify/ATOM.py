# Requires spotipy to be installed
# Made by Jahsias W
import time
from io import BytesIO
from subprocess import call

# Help With Genius
import requests
import spotipy
import spotipy.util as util
# Picture
from PIL import Image

# Your app's Client Id and Client Secret
# Found on Spotify
cid = ''
secret = ''

# Your username on Spotify
username = ""

# Can be any url
scope = "user-read-currently-playing"
redirect_uri = "http://localhost:8888/call"

oldSong = ''
# Runs Forever...
while True:

    # Requires popup for authentication, only requires once after cached
    token = util.prompt_for_user_token(username, scope, cid, secret, redirect_uri)

    # Creates a new Spotipy object
    sp = spotipy.Spotify(auth=token)

    # Gets the current song being played and the artist
    data = sp.current_user_playing_track()
    currentSong = data['item']['name']

    # Checks if a new song is playing
    if currentSong != oldSong:
        currentArtist = data['item']['artists'][0]['name']
        currentPicture = data['item']['album']['images'][0]['url']
        currentDemoSoundLink = data['item']['preview_url']
        currentPopularity = data['item']['popularity']
        oldSong = currentSong

        # Creates a .jpg of the current song's album picture
        response = requests.get(currentPicture)
        image = Image.open(BytesIO(response.content))
        i = image.save("spotifyPic.jpg")


        def popularity():
            if currentPopularity >= 100:
                return "the most popular song right now (Top"
            elif currentPopularity >= 95:
                return "extremely popular (Top"
            elif currentPopularity >= 85:
                return "very popular (Top"
            elif currentPopularity >= 50:
                return "somewhat popular (Top"
            elif currentPopularity >= 25:
                return "not very popular (Bottom"
            elif currentPopularity >= 2:
                return "not popular at all (Bottom"
            else:
                return "not listened to by anyone"


        # Finds how popular the song is
        result = popularity()

        # Genius API
        def request_song_info(song_title, artist_name):
            base_url = 'https://api.genius.com'
            headers = {'Authorization': 'Bearer ' + 'jpwdrAO_8VadWCwhnGdMqeDOERvKQ94QQM9oqcrkktRvNkZHPQzuPsLS2WMmPuv6'}
            search_url = base_url + '/search'
            genius_data = {'q': song_title + ' ' + artist_name}
            genius_response = requests.get(search_url, data=genius_data, headers=headers)

            return genius_response


        # Search for matches in the request response
        response = request_song_info(currentSong, currentArtist)
        json = response.json()
        remote_song_info = None

        # Finds the current song on with Genius
        for hit in json['response']['hits']:
            if currentArtist.lower() in hit['result']['primary_artist']['name'].lower():
                remote_song_info = hit
                break

        # Gets the song description
        # Need to scrape :(
        from bs4 import BeautifulSoup

        def scrap_song_url(url):
            # Gets the page URL
            page = requests.get(url)

            # All of the pages HTML
            html = BeautifulSoup(page.text, 'html.parser')

            # Removes added scripts from the HTML
            [h.extract() for h in html('script')]

            # Gets the song description
            p_tags = html.findAll("p")
            print(p_tags)

            # Removes extra information at the start
            if len(p_tags) > 2:
                new_tags = p_tags[2:]
            else:
                new_tags = p_tags[1:]

            text = ''
            for element in new_tags:
                text += ' ' + ''.join(element.findAll(text=True))

            return text


        # Checks if the song was found or not
        if remote_song_info:
            song_url = remote_song_info['result']['url']
            # Gets the songs description on Genius
            songDescription = scrap_song_url(song_url)
        else:
            songDescription = "\nCouldn't find track bio on Genius"

        # Removes occasional whitespace at the beginning of the string
        if songDescription[0].isspace:
            songDescription = songDescription[1:]

        # Removes occasional header text
        if songDescription[0:12] == "Release Date":
            songDescription = songDescription[13:]

        if songDescription == "":
            songDescription = "\nCouldn't find track bio on Genius"

        # Shortens description to fit 280 character limit
        currentTweetLength = len(currentSong) + len(currentArtist) + len(result) + 60
        tweetLength = 280
        charactersRemaining = tweetLength - currentTweetLength
        songDescriptionShort = songDescription[:charactersRemaining]

        # Removes all characters that display incorrectly on Twitter
        whitelist = set('abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789#.,()$')
        currentSong = ''.join(filter(whitelist.__contains__, currentSong))
        currentArtist = ''.join(filter(whitelist.__contains__, currentArtist))
        finalDescription = ''.join(filter(whitelist.__contains__, songDescriptionShort))

        # Outputs the result to a text file
        result = currentSong + " by " + currentArtist + "\nIt's " + result + " " + str(
            currentPopularity) + " percentile)\n" + finalDescription + "..."

        f = open("output.txt", "w+")
        f.write(result)
        f.close()

        # Calls the .js file to tweet
        print('Calling to Twitter...')
        call(["node", "../Twitter/index.js"])

    # Waits 5 seconds before seeing if a new song is playing
    time.sleep(5)
