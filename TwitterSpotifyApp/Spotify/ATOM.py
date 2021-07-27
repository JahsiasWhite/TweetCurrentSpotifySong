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
SPOTIFY_CLIENT_ID = ''
SPOTIFY_CLIENT_SECRET = ''

# Your username on Spotify
SPOTIFY_USERNAME = ""

# Can be any url
scope = "user-read-currently-playing"
redirect_uri = "http://localhost:8888/call"

# Makes sure all credentials are set
while SPOTIFY_CLIENT_ID == '':
    print("No client ID is provided")
    print("Please enter your client ID...")
    SPOTIFY_CLIENT_ID = input()

while SPOTIFY_CLIENT_SECRET == '':
    print("No client secret is provided")
    print("Please enter your client secret...")
    SPOTIFY_CLIENT_SECRET = input()

old_song = ''
# Runs Forever...
while True:

    # Requires popup for authentication, only requires once after cached
    token = util.prompt_for_user_token(SPOTIFY_USERNAME, scope, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, redirect_uri)

    # Creates a new Spotipy object
    sp = spotipy.Spotify(auth=token)

    # Gets the current song being played and the artist
    data = sp.current_user_playing_track()
    current_song = data['item']['name']

    # Checks if a new song is playing
    if current_song != old_song:
        current_artist = data['item']['artists'][0]['name']
        current_picture = data['item']['album']['images'][0]['url']
        current_demo_sound_link = data['item']['preview_url']
        current_popularity = data['item']['popularity']
        old_song = current_song

        # Creates a .jpg of the current song's album picture
        response = requests.get(current_picture)
        image = Image.open(BytesIO(response.content))
        i = image.save("spotifyPic.jpg")


        def popularity():
            if current_popularity >= 100:
                return "the most popular song right now (Top"
            elif current_popularity >= 95:
                return "extremely popular (Top"
            elif current_popularity >= 85:
                return "very popular (Top"
            elif current_popularity >= 50:
                return "somewhat popular (Top"
            elif current_popularity >= 25:
                return "not very popular (Bottom"
            elif current_popularity >= 2:
                return "not popular at all (Bottom"
            else:
                return "not listened to by anyone"


        # Finds how popular the song is
        popularity_result = popularity()

        # Genius API
        def request_song_info(song_title, artist_name):
            base_url = 'https://api.genius.com'
            headers = {'Authorization': 'Bearer ' + 'jpwdrAO_8VadWCwhnGdMqeDOERvKQ94QQM9oqcrkktRvNkZHPQzuPsLS2WMmPuv6'}
            search_url = base_url + '/search'
            genius_data = {'q': song_title + ' ' + artist_name}
            genius_response = requests.get(search_url, data=genius_data, headers=headers)

            return genius_response


        # Search for matches in the request response
        response = request_song_info(current_song, current_artist)
        json = response.json()
        remote_song_info = None

        # Finds the current song on with Genius
        for hit in json['response']['hits']:
            if current_artist.lower() in hit['result']['primary_artist']['name'].lower():
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
        currentTweetLength = len(current_song) + len(current_artist) + len(popularity_result) + 60
        tweetLength = 280
        charactersRemaining = tweetLength - currentTweetLength
        songDescriptionShort = songDescription[:charactersRemaining]

        # Removes all characters that display incorrectly on Twitter
        whitelist = set('abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789#.,()$')
        current_song = ''.join(filter(whitelist.__contains__, current_song))
        current_artist = ''.join(filter(whitelist.__contains__, current_artist))
        finalDescription = ''.join(filter(whitelist.__contains__, songDescriptionShort))

        # Outputs the result to a text file
        popularity_result = current_song + " by " + current_artist + "\nIt's " + popularity_result + " " + str(
            current_popularity) + " percentile)\n" + finalDescription + "..."

        f = open("output.txt", "w+")
        f.write(popularity_result)
        f.close()

        # Calls the .js file to tweet
        print('Calling to Twitter...')
        call(["node", "../Twitter/index.js"])

    # Waits 5 seconds before seeing if a new song is playing
    time.sleep(5)
