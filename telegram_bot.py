import requests
from tweepy_streamer import *

from config import TELEGRAM_SEND_MESSAGE_URL

class TelegramBot:

    def __init__(self):

        self.chat_id = None
        self.text = None
        self.first_name = None
        # self.last_name = None


    def parse_webhook_data(self, data):

        message = data['message']

        self.chat_id = message['chat']['id']
        self.incoming_message_text = message['text'].lower()
        self.first_name = message['from']['first_name']
        
        # self.last_name = message['from']['last_name']


    def action(self):

        success = None

        tc=TwitterClient()
        ta=TweetAnalyser()


        api=tc.get_twitter_client_api()

        if self.incoming_message_text == '/start':
            self.outgoing_message_text = "Hi {}! I am Sentiment analyser bot! I analyse twitter data after carrying out Natural Language Processing!".format(self.first_name)
            success = self.send_message() 

        if self.incoming_message_text == '/hello':
            self.outgoing_message_text = "Hello {}!".format(self.first_name)
            success = self.send_message()

        elif self.incoming_message_text == '/help':
            self.outgoing_message_text = 'Choose any one:\n\n1. /gettweets_<some_twitter_handle> \n\tTo fetch recent tweets.\n\n2. /getretweets_<some_twitter_handle> \n\t To fetch number of retweets\n\n3. /analysetweets_<some_twitter_handle> \n\tTo analyse tweets using NLP and get sentiment score ranging from  -1 to 1'
            success = self.send_message()

        elif '/gettweets_' in self.incoming_message_text:
            twitter_handle=self.incoming_message_text[11:]
            tweets=api.user_timeline(screen_name=twitter_handle)
            df=ta.tweets_to_data_frame(tweets)
            self.outgoing_message_text = df['Tweets'].head(10)
            success = self.send_message()

        elif '/getretweets_' in self.incoming_message_text:
            twitter_handle=self.incoming_message_text[13:]
            tweets=api.user_timeline(screen_name=twitter_handle, count=100)
            df=ta.tweets_to_data_frame(tweets)
            self.outgoing_message_text = df['retweets'].head(10)
            success = self.send_message()


        elif '/analysetweets_' in self.incoming_message_text:
            twitter_handle=self.incoming_message_text[len('/analysetweets_'):]
            tweets=api.user_timeline(screen_name=twitter_handle)
            df=ta.tweets_to_data_frame(tweets)
            df['sentiment']=np.array([ta.analyse_sentiment(tweet) for tweet in df['Tweets']])
            self.outgoing_message_text = df.head(10)
            success = self.send_message()
        return success


    def send_message(self):
        
        res = requests.get(TELEGRAM_SEND_MESSAGE_URL.format(self.chat_id, self.outgoing_message_text))

        return True if res.status_code == 200 else False
    

    @staticmethod
    def init_webhook(url):
        
        requests.get(url)


