#!/usr/bin/env python
# encoding: utf-8

import time
import os

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

ckey = os.environ.get('ckey')
csecret = os.environ.get('csecret')
atoken = os.environ.get('atoken')
asecret = os.environ.get('asecret')

class listener(StreamListener):

	def on_data(self, data):
		try:
			print data
			saveFile = open('data/NYCTtweets_feb_forward.json', 'a')
			saveFile.write(data)			
			saveFile.write('\n')
			saveFile.close()
			return True
		except BaseException, e:
			print 'failed ondata,',str(e)
			time.sleep(10)

	def on_error(self, status):
		print status

try:
	auth = OAuthHandler(ckey, csecret)
	auth.set_access_token(atoken, asecret)
	twitterStream = Stream(auth, listener())
	twitterStream.filter(follow=['66379182']) # account_id for @NYCTSubway account. Records tweets from the account, to the account, and replies.
except BaseException, e:	
	print 'failed authorization,',str(e)