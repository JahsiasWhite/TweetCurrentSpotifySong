//Creates Twit object requiring node install twit
var Twit = require('twit');

//Your app's Consumer Key, Consumer Secret, Acess Token, and Access Token
var T = new Twit({
	consumer_key:   ''                              // API Key
	, consumer_secret:  '' // API Secret Key
	, access_token:    '-'  // Access Token
	, access_token_secret: ''   // Access Token Secret
});

/* Gets the current song being played */
const fs = require('fs');
var input = "../Spotify/output.txt";

//Tweets
readFile(input);

function readFile(callback) {
fs.readFile(input, (err, data) => {
	if (err) throw err;
	var result = "I'm listening to\n" +data.toString();

	var b64content = fs.readFileSync('../Spotify/spotifyPic.jpg', { encoding: 'base64' })
	T.post('media/upload', { media_data: b64content }, function (err, data, response) {

	/* Sets up parameters for tweeting */
	var mediaIdStr = data.media_id_string
	var altText = "Current Songs Cover Art"
	var meta_params = { media_id: mediaIdStr, alt_text: { text: altText } }

	/* Tweets */
	T.post('media/metadata/create', meta_params, function (err, data, response) {
	if (!err) {
		var params = { status: result, media_ids: [mediaIdStr] }
		T.post('statuses/update', params, function (err, data, response) {
			console.log('Tweeted')
		})
	}
})
})
});
}



