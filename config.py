# tweepy-bots/bots/config.py
import tweepy

def create_api():
    consumer_key = "lnJ0Ob8706AXHYqGMdiSTT5AM"
    consumer_secret = "ny3cBX6yUTKJ7KfPyYOxffA1lACBivQA6PCqjYG6hTVOO07UDN"
    access_token = "1090395238340866049-LuttJLQCkra0E868UBoM31ageyZDoy"
    access_token_secret = "609SZbv8rmogwXK7YAChfMTmfaKXQTChbHrOVaIHqaLsg"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth, wait_on_rate_limit=True)

    return api


