#!/usr/bin/python

''' 
A twitter bot

'''

import API_Tokens as t
import json
from tweepy import OAuthHandler, API, Stream
from tweepy.streaming import StreamListener
import os
import time
import datetime

class listener(StreamListener):
	pass

def main():
	#Authentication of API and print self Info
	api = authenticate()
	selfInfo(api)
	flag=True
	while(flag==True):
		flag = options(api)

def authenticate():
	''' Authenticate the use of twitter API '''
	auth = OAuthHandler(t.CONSUMER_KEY, t.CONSUMER_SECRET)
	auth.set_access_token(t.ACCESS_TOKEN,t.ACCESS_TOKEN_SECRET)
	api = API(auth)
	return api

def options(api):
	print '\nSelect an option from below: '
	print '---------------------------- '
	print "\n1.View your Timeline\n2.Post a new tweet\n3.View your tweets\n4.Quit\n"
	option = int(input())
	

	if option == 1:
		''' Views the user's timeline, recent 20 tweets, more tweets can be loaded. '''

		#initial variables
		raw_tweets, tweets =[], []
		first_tweet_id, last_tweet_id = -1, -1
		count =0
		opt = True
		
		#default timeline, loads first 20 tweets
		temp = api.home_timeline()
		raw_tweets.extend(temp)
		
		#keep track of the most recent and the last tweet id
		last_tweet_id = int(raw_tweets[-1].id -1)
		first_tweet_id = int(raw_tweets[0].id)
			
		
		while opt is True:
			if count == 1:		
				#loads 20 more older tweets after last_tweet_id, also adjusts last_tweet_id
			    temp = api.home_timeline(max_id = last_tweet_id)
			    raw_tweets.extend(temp)
			    last_tweet_id = int(temp[-1].id-1)

			if count == 2:
				#loads 20 more newer tweets after first_tweet_id, also adjusts first_tweet_id
			    temp = api.home_timeline(since_id = first_tweet_id)
			    raw_tweets.extend(temp)
			    try:
			        first_tweet_id = int(temp[0].id)
			    except:
			    	print '\nNo new tweets.'
			print '\n'

			#prints and stores the tweets in the list "tweets"
			tweets.extend(printTweets(temp,favorite_count=True,retweet_count=True))

			#further options
			print '\nOptions:\n--------\n\n1.Load older tweets\n2.Load newer tweets\n3.Dump tweets to a file\n4.Main Menu\n5.Quit'
						
			sub_option = int(input())

			if sub_option == 1:
				count=1
				continue

			if sub_option ==2:
				count=2
				continue

			if sub_option == 3:
				dumpTweetsToFile(tweets)
				return True

			if sub_option == 4:
				return True

			if sub_option ==5:
				return False

			else:			## Make more robust!!
				print '\nInvalid choice!\n'
				return True


	if option == 2:
		''' Posting tweets on twitter '''

		#Attaching with media
		media = raw_input('\nAttach media? (Y/N): ')
		yes_optn = ['y','Y','yes','YES','Yes']
		if media in yes_optn:
			path = raw_input('\n Enter path of the media (image/video): ')
		
		#tweet body
		while True:
		    status = raw_input("\nWhat's happening?\n----------------\n\n")

		    if (len(status) > 140):
		    	#tweet size exceeds 140 characters!
		    	print 'tweet exceeds 140 characters!!'
		    	post = raw_input(" type 'c' to change your tweet, 'p' to post your tweet: ")
		    	if (post == "c" or post == 'C'):
		    		continue
		    	elif (post=='p' or post == 'P'):
		    		status = status[:137] + "..."
		    		pass
		    	else:
		    		print 'Invalid choice!\n'
		    		return True

		    if media in yes_optn:
		    	#only runs if media is present
		    	try:
		    	    api.update_with_media(filename=path,status=status)
		    	    print '\nTweet was successful!!\n\n'
		    	except Exception as e:
		    		print 'Error occured!\n ' + e
		    	finally:
		    	    break
    
		    else:
		    	try:
		    	    api.update_status(status)
		    	    print '\nTweet was successful!!\n\n'
		    	except Exception as e:
		    		print 'Error occured!\n ' + e
		    	finally:
		    	    break
		return True

	if option == 3:
		''' Views the user's own recent 20 tweets, more tweets can be loaded. '''

		#initial variables
		raw_tweets, tweets =[], []
		first_tweet_id, last_tweet_id = -1, -1
		count = 0
		opt = True

		#default timeline, loads first 20 tweets
		temp = api.user_timeline()
		raw_tweets.extend(temp)
		
		#keep track of the most recent and the last tweet id
		last_tweet_id = int(raw_tweets[-1].id -1)
		first_tweet_id = int(raw_tweets[0].id )
			
		while opt is True:
			
			if count == 1:
				#loads 20 more older tweets after last_tweet_id, also adjusts last_tweet_id
			    temp = api.user_timeline(max_id = last_tweet_id)
			    raw_tweets.extend(temp)
			    last_tweet_id = int(temp[-1].id-1)

			if count == 2:
				#loads 20 more newer tweets after first_tweet_id, also adjusts first_tweet_id
			    temp = api.user_timeline(since_id = first_tweet_id)
			    raw_tweets.extend(temp)
			    try:
			        first_tweet_id = int(temp[0].id)
			    except:
			    	print '\nNo new tweets.'
			print '\n'

			#prints and stores the tweets in the list "tweets"
			tweets.extend(printTweets(temp,favorite_count=True,retweet_count=True))

			#further options
			print '\nOptions:\n--------\n\n1.Load older tweets\n2.Load newer tweets\n3.Dump tweets to a file\n4.Main Menu\n5.Quit'
						
			sub_option = int(input())

			if sub_option == 1:
				count=1
				continue

			if sub_option ==2:
				count=2
				continue

			if sub_option == 3:
				dumpTweetsToFile(tweets)
				return True

			if sub_option == 4:
				return True

			if sub_option ==5:
				return False

			else:			## Make more robust!!
				print '\nInvalid choice!\n'
				return True

	if option == 4:
		return False

	else:
		print '\nInvalid option!\n'
		return True


def dumpTweetsToFile(tweets):
	''' dumps all the tweets in the list tweets in a file tweets.txt with timestamp. '''
	with open("tweets.txt","a") as f:
		timestamp = str(datetime.datetime.now())
		f.write("Tweet Dump on " + timestamp + ':\n--------------' + '-'*int(len(timestamp)) + '--\n\n')
		for tweet in tweets:
			f.write(tweet.encode("UTF-8") + "\n\n")

	print '\nTweet dump successful!!!\n\n'
	return

def printTweets(tweet_data,screen_name=True,text=True,created_at=True,retweet_count=False,favorite_count=False,lang=False):
	''' prints out tweets from raw tweet data recieved from the api and returns a list of structured tweets. '''
	list_of_tweets =[]
	for t in tweet_data:
		s=""
		tweet = json.dumps(t._json)
		j = json.loads(tweet)
		time.sleep(.3)
		if screen_name == True:
			s+= j['user']['screen_name'] + " "
		if screen_name==False and created_at==True:
			s+= 'Created on: ' + j['created_at'][:-11] 
		if screen_name==True and created_at==True:
			s+= 'on: ' + j['created_at'][:-11]
		if lang == True:
			s+= " ; language: " + j['lang']
		if text==True:
			s+= "\n" + j['text'] + "\n"
		if retweet_count == True:
			s+= '    Retweets: ' + str(j['retweet_count'])
		if favorite_count == True:
			s+= '    Favorites: ' + str(j['favorite_count'])
		s+= "\n"
		print s
		list_of_tweets.append(s)

	return list_of_tweets

def selfInfo(api):
	'''print information about authenticated user '''
	user = api.me()

	#get current window size
	columns = os.popen('stty size', 'r').read().split()[1]

	#Display user information
	print
	print '{:^{}}'.format("======================",columns)
	print "{:^{}}".format("|| User-Information ||",columns)
	print '{:^{}}'.format("======================",columns)
	print "\n"+"{:^{}}".format(user.name,columns) + '\n' + "{:^{}}".format("@"+user.screen_name,columns) + '\n  ' + "{:^{}}".format(user.description,columns)
	print '='*int(columns) + "\n"
	return



if __name__ == '__main__':
	main()