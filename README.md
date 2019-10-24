# Sentiment Analyser Bot

![](https://github.com/smitgajjar/sentiment_analyser_bot/blob/master/start_help_command.gif)

### What is it?
A chatbot, which analyses polarity of recent tweets of some given twitter handle. It classifies sentiment of the tweets into negative, neutral or positive calibre. (replies in the range of -1 to +1)

### How it works?
- The core of this project lies in the trained ML model of TextBlob module, which does our amazing work of Natural Language Processing of tweets.
- Tweepy fetches required tweets at real time.
- Flask handles the backend of our chatbot.
- Ngrok hosts our bot on https server temporarily.

### Prerequistes:
- Python 3.7
- Flask
- Twitter API
- Tweepy
- TextBlob
- Telegram bot API
- Numpy
- ngrok

### How to create your own bot and use it?
- Clone this repository
- Download ngrok into this project directory: https://ngrok.com/download
- Add your twitter API credentials in twitter_credentials.py file
- Now, fire up the terminal and type the following:
```
username@username-PC: ~/myrepository$ ./ngrok http 5000
```
- Add your telegram bot token in config.py file
- Add your ngrok https URL (as obtained in the terminal output) in config.py file
- Run the Flask server:
```
username@username-PC: ~/myrepository$ python3 app.py
```

There you go !!!

Go ahead, play with your bot!

![](https://github.com/smitgajjar/sentiment_analyser_bot/blob/master/analysetweets_command.gif)