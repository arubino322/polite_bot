import os
import re
import json
import joblib
import numpy as np

from datetime import datetime, timedelta

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy import API
from tweepy.streaming import StreamListener

from nltk.tokenize import TweetTokenizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer

from tweet_responses import positive_responses, negative_responses

ckey = os.environ.get('pb_ckey')
csecret = os.environ.get('pb_csecret')
atoken = os.environ.get('pb_atoken')
asecret = os.environ.get('pb_asecret')

tokenizer = TweetTokenizer(strip_handles=True, 
                           preserve_case=False,
                           reduce_len=True)

# instantiate vader object
sid = SentimentIntensityAnalyzer()

def read_pickle_files(filepath=None):
    inst = open(filepath, "rb")
    pipeline = joblib.load(inst)
    inst.close()
    return pipeline

mnb_pipeline = read_pickle_files("./pickle_files/vectorizer_and_mnb.pkl")
log_pipeline = read_pickle_files("./pickle_files/vectorizer_and_logreg.pkl")
sgd_pipeline = read_pickle_files("./pickle_files/vectorizer_and_sgd.pkl")


class listener(StreamListener):
    def __init__(self):
        self.stopwords = ['i','me','my','myself','we','our','ours','ourselves','you',"you're","you've","you'll","you'd",'your','yours','yourself','yourselves','he','him','his','himself',
                        'she',"she's",'her','hers','herself','it',"it's",'its','itself','they','them','their','theirs','themselves','what','which','who','whom','this','that',"that'll",
                        'these','those','am','is','are','was','were','be','been','being','have','has','had','having','do','does','did','doing', 'a','an','the','and','but','if','or','because',
                        'as','until','while','of','at','by','for','with','about','against','between','into','through','during','before','after','above','below','to','from','up','down','in',
                        'out','on','off','over','under','again','further','then','once','here','there','when','where','why','how','all','any','both','each','few','more','most','other',
                        'some','such','no','nor','not','only','own','same','so','than','too','very', 's', 't','can','will','just','don',"don't",'should',"should've",'now', 'd','ll', 
                        'm', 'o','re','ve', 'y','ain','aren',"aren't",'couldn',"couldn't",'didn',"didn't",'doesn',"doesn't",'hadn',"hadn't",'hasn',"hasn't",'haven',"haven't",'isn',
                        "isn't",'ma','mightn',"mightn't",'mustn',"mustn't",'needn',"needn't",'shan',"shan't",'shouldn',"shouldn't",'wasn',"wasn't",'weren',"weren't",'won',"won't",
                        'wouldn',"wouldn't",'rt', 'nyctsubway']

    def check_json_key_value(self, data):
        if json.loads(data).get('extended_tweet') != None:
            return json.loads(data).get('extended_tweet').get('full_text')
        else:
            return json.loads(data).get('text')

    def get_tweet_id(self, data):
        return json.loads(data).get('id_str')

    def tokenize_and_transform(self, tweet):
        # remove punctuations
        tweet = re.sub(r'[^\w\s]','',tweet)
        # tokenize
        stripped = [w for w in tokenizer.tokenize(tweet) if w not in self.stopwords]
        return ' '.join(stripped)

    def do_the_models_agree(self, pred1, pred2, pred3):
        if pred1 == pred2 == pred3:
            if pred1 == 'negative':
                return 'all_negative'
            if pred1 == 'positive':
                return 'all_positive'
        else:
            return 'no'

    def how_should_we_respond(self, compound_score, do_they_agree, tweet_text):
        if compound_score >= 0.45 and do_they_agree == 'all_positive':
            return positive_responses(tweet_text)
        elif compound_score <= -0.75 and do_they_agree == 'all_negative':
            return negative_responses(tweet_text)

    def reply(self, response, tweeter, tweet_id):
        if response != None:
            return api.update_status(status="@NYCTSubway @{} {}".format(tweeter, response),
                                     in_reply_to_status_id="{}".format(tweet_id))

    def on_data(self, data):
        try:
            tweet = self.check_json_key_value(data)
            tweeter = json.loads(data).get('user').get('screen_name')
            tokenized = self.tokenize_and_transform(tweet)
            tweet_id = self.get_tweet_id(data)
            mnb_prediction = mnb_pipeline.predict([tokenized])[0]
            log_prediction = log_pipeline.predict([tokenized])[0]
            sgd_prediction = log_pipeline.predict([tokenized])[0]
            do_they_agree = self.do_the_models_agree(mnb_prediction, log_prediction, sgd_prediction)
            if do_they_agree != 'no':
                print(tweet_id)
                print('Created at: {}'.format(json.loads(data).get('created_at')))
                print('Tweeter: {}'.format(tweeter))
                print('In reply to: {}'.format(json.loads(data).get('in_reply_to_screen_name')))
                print(tweet)
                print("Multinomial Naive Bayes Prediction: {}".format(mnb_prediction))
                print("Logistic Regression Prediction: {}".format(log_prediction))
                print("Stochastic Gradient Descent Prediction: {}".format(sgd_prediction))
                print(self.do_the_models_agree(mnb_prediction, log_prediction, sgd_prediction))
                # compound VADER score
                compound_score = sid.polarity_scores(tokenized)['compound']
                print("VADER Compound Score: {}".format(compound_score))
                # How should we respond?
                response = self.how_should_we_respond(compound_score, 
                                                      self.do_the_models_agree(mnb_prediction, log_prediction, sgd_prediction),
                                                      tweet)
                print("Response: {}".format(response))
                self.reply(response, tweeter, tweet_id)
            print('-'*75)
            if json.loads(data).get('in_reply_to_screen_name') == 'NYCTSubway':
                saveFile = open('./data/nyctsubway_stream_oct10_on.csv', 'a')
                saveFile.write(data)
                saveFile.write('\n')
                saveFile.close()
                return True
        except BaseException:
            print('failed ondata')
            time.sleep(5)

    def on_error(self, status):
        print(status)



try:
    auth = OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken, asecret)
    # tweepy api class
    api = API(auth)
    twitterStream = Stream(auth, listener())
    twitterStream.filter(track=['@NYCTSubway'])
except BaseException:
    print('failed authorization')
