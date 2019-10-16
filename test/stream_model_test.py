import os
import json
import joblib

from datetime import datetime, timedelta

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

from nltk.tokenize import TweetTokenizer
# from nltk.corpus import stopwords

ckey = os.environ.get('ckey')
csecret = os.environ.get('csecret')
atoken = os.environ.get('atoken')
asecret = os.environ.get('asecret')


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
                        'wouldn',"wouldn't",'rt']


    def tokenize_and_transform(self, tweet):
        
        stripped = [w for w in tokenizer.tokenize(tweet) if w not in self.stopwords]
        return ' '.join(stripped)

    def on_data(self, data):
        try:
            print('Created at: {}'.format(json.loads(data).get('created_at')))
            print('Tweeter: {}'.format(json.loads(data).get('user').get('screen_name')))
            print('In reply to: {}'.format(json.loads(data).get('in_reply_to_screen_name')))
            if json.loads(data).get('extended_tweet') != None:
                print(json.loads(data).get('extended_tweet').get('full_text'))
                print(self.tokenize_and_transform(json.loads(data).get('extended_tweet').get('full_text')))
            else:
                print(json.loads(data).get('text'))
                # print('Tokenized: {}'.format(tokenizer.tokenize(json.loads(data).get('text'))))
                print(self.tokenize_and_transform(json.loads(data).get('text')))
            print('-'*75)
            if json.loads(data).get('in_reply_to_screen_name') == 'NYCTSubway':
                saveFile = open('../data/nyctsubway_stream_oct10_on.csv', 'a')
                saveFile.write(data)
                saveFile.write('\n')
                saveFile.close()
            return True
        except BaseException:
            print('failed ondata')
            time.sleep(5)

    def on_error(self, status):
        print(status)


#Loading the saved MNB, LOGREG, SGD models with joblib
classifier_f1 = open("../pickle_files/vectorizer_and_mnb.pkl", "rb")
mnb_pipeline = joblib.load(classifier_f1)
classifier_f1.close()

classifier_f2 = open("../pickle_files/vectorizer_and_logreg.pkl", "rb")
log_pipeline = joblib.load(classifier_f2)
classifier_f2.close()

classifier_f3 = open("../pickle_files/vectorizer_and_sgd.pkl", "rb")
sgd_pipeline = joblib.load(classifier_f3)
classifier_f3.close()

tokenizer = TweetTokenizer(strip_handles=True, 
                           preserve_case=False,
                           reduce_len=True)


def remove_punctuations(row):
    return re.sub(r'[^\w\s]','',row)

try:
    auth = OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken, asecret)
    twitterStream = Stream(auth, listener())
    twitterStream.filter(track=['@NYCTSubway'])
except BaseException:
    print('failed authorization')
