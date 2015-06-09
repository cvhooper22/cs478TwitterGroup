#Import the necessary methods from tweepy library
from tweepy import OAuthHandler
from tweepy import API
from unidecode import unidecode
import json

#Variables that contain the user credentials to access Twitter API 
access_token = "ENTER TOKEN HERE"
access_token_secret = "ENTER TOKEN HERE"
consumer_key = "ENTER TOKEN HERE"
consumer_secret = "ENTER TOKEN HERE"

if __name__ == '__main__':
	
	keywordsArray = []
	keywordsPath = "keywords.txt"
	with open(keywordsPath, "r") as f:
		for keywordLine in f:
			keywordsArray.append(unidecode(keywordLine.strip()))
	
	#print keywordsArray
	#This handles Twitter authetification
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = API(auth_handler=auth, wait_on_rate_limit=True)
	#need to use the API.user_timeline(user_id, count) method
	screenName = "NAFISZ"
	public_tweets = api.user_timeline(screen_name=screenName, count=100)
	
	for tweet in public_tweets:
		filename = ("usertweets.txt")
		with open(filename, "a") as f:
			f.write(json.dumps(tweet._json).encode('utf8') + "\n\n")