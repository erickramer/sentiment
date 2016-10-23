from bs4 import BeautifulSoup
import requests
import twitter
import config
import time

EMOJI_URL = 'http://unicode.org/emoji/charts/emoji-list.html'

class EmoticonStream(object):

    def __init__(self, nb_emoji=98,
                positive=range(1,21), negative=range(47, 66)):

        self._emojis = []
        self._positive_emojis = []
        self._negative_emojis = []

        res = requests.get(EMOJI_URL)
        bs = BeautifulSoup(res.content, 'html.parser')

        for row in bs.find_all('tr')[::-1]:
            i = row.find_next(attrs='rchars').text
            emoji = row.find_next(attrs="chars").text

            try:
                i = int(i)
                if i <= nb_emoji:
                    self._emojis.append(emoji)
                    if i in positive:
                        self._positive_emojis.append(emoji)
                    elif i in negative:
                        self._negative_emojis.append(emoji)
                else:
                    break
            except ValueError:
                pass

        self._api = twitter.Api(consumer_key=config.consumer_key,
                                consumer_secret=config.consumer_secret,
                                access_token_key=config.access_token,
                                access_token_secret=config.access_token_secret)

        self._stream = self._api.GetStreamFilter(track=self._emojis)

    def __iter__(self):
        return self

    def next(self):
        while True:
            try:
                tweet = self._stream.next()
                try:
                    raw_text = tweet['text']
                    emojis = self._find_emojis(raw_text)
                    text = self._strip_emojis(raw_text)
                    return raw_text, text, emojis
                except KeyError:
                    pass
            except StopIteration:
                self._restart_stream()

    def _reset_stream(self):
        time.sleep(1)
        self._stream = self._api.GetStreamFilter(track=self._emojis)

    def _strip_emojis(self, text):
        for e in self._emojis:
            text = text.strip(e)
        return text

    def _find_emojis(self, text):
        return [e for e in self._emojis if e in text]
