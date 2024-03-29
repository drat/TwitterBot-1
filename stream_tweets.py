#!/usr/bin/python

''' 
Fetches streaming tweets in real time.
'''

import API_Tokens as t
import json
from tweepy import OAuthHandler, API
from tweepy.streaming import StreamListener
from tweepy import Stream
import os

### Custom made listener Class; deals with all the incoming streaming data
class MyListener(StreamListener):

	def __init__(self):
		pass

	# Write all the incoming data in buffer.json file
	def on_data(self,data):
		try:
			with open("tweets.json","a") as f:
				j = json.loads(data)
				#See Twitter reference for what fields are included -- https://dev.twitter.com/docs/platform-objects/tweets
				line1 = "@" + str(j['user']['screen_name']) + " on " + j['created_at'][:-11] + ", language= "+ j["lang"] + ": "
				line2 = '\n' + j['text']
				text = line1 + line2
				print text + "\n\n"

				# writes the streamed data to tweets.json
				# if you want to save the tweets only, replace "data" with "text" in the line below
				f.write(data + "\n\n")
				

		except Exception as e:
			print "Error: " +str(e)
		return True

	def on_error(self,status):
		print status
		return True


def main():
	#creating a REST_API instance
	api, auth = authenticate()

	try:
		#creating Streaming_API instance
		stream = Stream(auth, MyListener())
		selfInfo(api)  ## Show self information
		
		#search query
		query = raw_input('Search query: ')
		print "\nTweets:"
		print "-------\n\n"
		stream.filter(track = [query])

	except KeyboardInterrupt:
		print '\n Stopped Fetching Tweets.'
		exit()

def authenticate():
	''' Authentication for using twitter data '''
	auth = OAuthHandler(t.CONSUMER_KEY, t.CONSUMER_SECRET)
	auth.set_access_token(t.ACCESS_TOKEN,t.ACCESS_TOKEN_SECRET)
	api = API(auth)
	return api, auth

def selfInfo(api):
	'''print information about authenticated user '''
	user = api.me()
	columns = os.popen('stty size', 'r').read().split()[1]
	print '{:^{}}'.format("======================",columns)
	print "{:^{}}".format("|| User-Information ||",columns)
	print '{:^{}}'.format("======================",columns)
	print "\n"+"{:^{}}".format(user.name,columns) + '\n' + "{:^{}}".format("@"+user.screen_name,columns) + '\n  ' + "{:^{}}".format(user.description,columns) 
	print "=" * int(columns) +"\n\n"
	return

if __name__ == '__main__':
	main()