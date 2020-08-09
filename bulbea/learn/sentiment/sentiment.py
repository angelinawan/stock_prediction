from __future__ import absolute_import

import textblob
import datetime
from datetime import date, timedelta
from Legacy.bulbea.learn import Twitter

def sentiment(share, *args, **kwargs):
    search = share.ticker
    tw=Twitter()
    ret=[]
    date_list=[]
    for i in range(7):
        cur = date.today() - timedelta(i)
        date_str = cur.strftime('%Y-%m-%d')
        date_list.append(cur)

        tweets = tw.API.search(search, until=date_str)
        score  = 0

        for tweet in tweets:
            blob   = textblob.TextBlob(tweet.text)
            score += blob.sentiment.polarity
        if(len(tweets)>0):
            ret.append(score / len(tweets))
        else:
            ret.append(0)
    return ret, date_list