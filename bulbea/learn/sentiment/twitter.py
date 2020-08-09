# imports - compatibility packages
from __future__ import absolute_import

# imports - third-party packages
import tweepy

# module imports
from Legacy.StockMaster.bulbea import AppConfig
from Legacy.StockMaster.bulbea import _check_environment_variable_set

class Twitter(object):
    def __init__(self):
        #access_token = "920108859007684608-UyNMjzKK1WL67bSkbI9nx7xLX4286nV"
        #access_token_secret = "nvwDEdY7a6MccvKFuQQvUmwcjadVKB4B7tc6aNwxRG7aw"
        #consumer_key = "RKlq1R5ug0JeQooH3VgwYglXa"
        #consumer_secret = "xwy29DNnp8SeoUwBdivi5KvW0UWGFctqZwqTZYr9k2ak25giO6"
        api_key                  = "RKlq1R5ug0JeQooH3VgwYglXa"
        api_secret               = "xwy29DNnp8SeoUwBdivi5KvW0UWGFctqZwqTZYr9k2ak25giO6"
        access_token             = "920108859007684608-UyNMjzKK1WL67bSkbI9nx7xLX4286nV"
        access_token_secret      = "nvwDEdY7a6MccvKFuQQvUmwcjadVKB4B7tc6aNwxRG7aw"

        #_check_environment_variable_set(api_key, raise_err = True)
        #_check_environment_variable_set(api_secret, raise_err = True)
        #_check_environment_variable_set(access_token, raise_err = True)
        #_check_environment_variable_set(access_token_secret, raise_err = True)

        self.api_key             = api_key
        self.api_secret          = api_secret
        self.access_token        = access_token
        self.access_token_secret = access_token_secret

        self.auth_handler        = tweepy.OAuthHandler(self.api_key, self.api_secret)
        self.auth_handler.set_access_token(self.access_token, self.access_token_secret)

        self.API                 = tweepy.API(self.auth_handler)

        #auth = tweepy.OAuthHandler(api_key, api_secret)
        #auth.set_access_token(access_token, access_token_secret)

        #self.API  = tweepy.API(auth)
