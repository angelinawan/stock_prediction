import sys
import os
import requests
import oauth2
import json
import string
import re
from unidecode import unidecode
import math
import schedule
import time
import codecs
import csv

def oauth_req(url, key, secret, http_method="GET", post_body="", http_headers=None):
    consumer = oauth2.Consumer(key="qOaznKRz5VhaSl7Cz6QYH2nB9", secret="LdvYknJa0WZroecT0k1KYdRi7UH8ot0K8HezT5OAC0uLaiTbJk")
    token = oauth2.Token(key="809904932-NnxQCbT29Y97CqdxRMhJMwrxs3DsiLi7Q3hx6nUJ", secret="Zwuw2pCGZopavmKHwbrswVuriCdVAjwY5OeOk97a1uWgT")
    client = oauth2.Client(consumer, token)
    resp, content = client.request( url, method=http_method, body=post_body, headers=http_headers )
    return content

def collectTweets(keyword):
    global tweet_text

    # search query for twitter api
    url = "https://api.twitter.com/1.1/search/tweets.json?q=" + keyword + "&result_type=recent&count=100"
    returned_tweets = oauth_req(url, 'abd', 'hey')

    # convert tweet from json to dictionary
    res = json.loads(returned_tweets)

    # collect all tweet text and tweeter follower count
    for status in res["statuses"]:
        tweet_text[status["id"]] = [status["text"], status["user"]["followers_count"]]
    # tweet_text.append(status["text"])

    # iterate through more pages in twitter to collect as many tweets as possible and store those as well
    for num in range(0, 100):
        if res is None:
            break
        if "next_results" not in res:
            break
        url = "https://api.twitter.com/1.1/search/tweets.json" + res["search_metadata"]["next_results"]
        returned_tweets = oauth_req(url, 'abd', 'hey')

        res = json.loads(returned_tweets)
        if res is None:
            break
        for status in res["statuses"]:
            tweet_text[status["id"]] = [status["text"], status["user"]["followers_count"]]

    return tweet_text
