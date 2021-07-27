# Tweets Current Spotify Song


## Description:

Uses the Spotify, Genius, and Twitter API to find the song you are currently listening to and Tweets out the song name, description about the song, and the cover art.
Uses python to get spotify and genius data every 5 seconds. The JS file then uses this info to post a tweet. <br>


## Running the software

### Clone Repository
``git clone https://github.com/JahsiasWhite/TweetCurrentSpotifySong.git``

### Install the needed packages
The requirements are listed in requirements.txt. Using pip, you can install all packages with
``pip3 install -r /path/to/requirements.txt``

### Set Parameters
You need both authorization from Spotify and Twitter

For Spotify,
1. Navigate to ATOM.py in TweetCurrentSpotifySong/TwitterSpotifyApp/Spotify

2. Go to 
``https://developer.spotify.com/``

3. Login and create a new app

4. Copy and paste parameters into ATOM.py
* Copy "Client Id" to cid         ``cid = '0f4a9e39a947421b8650f7a0842baefd'``
* Copy "Client Secret" to secret ``secret = 'd67ebb6b783e447c89d53175e8173851'``
* Enter your spotify username ``username = "John"``

For Twitter,
1. Navigate to index.js in ../TweetCurrentSpotifySong/TwitterSpotifyApp/Twitter

2. Go to 
``https://developer.twitter.com/en/portal/projects-and-apps``

3. Login and create a new app

4. Go to keys and tokens for the app

5. Copy and paste parameters into index.js
* Regenerate the API key and secret
* Copy API Key to consumer_key
* Copy API Secret Key to consumer_secret
* Regenerate the Access Token and Secret
* Copy Access Token to access_token
* Copy Access Token to access_token_secret

### Run it
1. Go to ../TweetCurrentSpotifySong/TwitterSpotifyApp/Spotify

2. Type
``ATOM.py``

If Spotify credentials weren't provided, they will be asked to be entered before the program continues. 
If the wrong Spotify credentials were entered a new tab will open on your webrowser saying which credential was wrongly entered. The program will also be stuck and has to be restarted if this happens

