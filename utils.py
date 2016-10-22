import numpy as np
import time
import re
import twitter
from twitter.parse_tweet import Emoticons
import config

def data_gen(emoticon_stream, text_encoder, emo_encoder, batch_size=100):
    xs = []
    ys_emo = []
    ys_pos = []

    for text, emoticons, positive in emoticon_stream:
        xs.append(text_encoder(text))
        ys_emo.append(emo_encoder(emo))
        ys_pos.append(positive)

        if len(xs) == batch_size:
            yield np.stack(xs), (np.stack(ys_emo), np.stack(ys_pos))
            xs = []
            ys_emo = []
            ys_pos = []

class EmoticonStream(object):

    def __init__(self, emoticons=None, timeout=None):
        if emoticons is None:
            self._emoticons = Emoticons.POSITIVE + Emoticons.NEGATIVE
        else:
            self._emoticons = emoticons

        self._api = twitter.Api(consumer_key=config.consumer_key,
                                consumer_secret=config.consumer_secret,
                                access_token_key=config.access_token,
                                access_token_secret=config.access_token_secret,
                                timeout=timeout)

        self._restart_stream()

    def __iter__(self):
        return self

    def _restart_stream(self):
        self._stream = self._api.GetStreamFilter(track=self._emoticons)

    def _strip_emoticons(self, text):
        for e in self._emoticons:
            text = text.strip(e)
        return text

    def _find_emoticons(self, text):
        return [e for e in self._emoticons if e in text]

    def next(self):
        text = None

        while True:
            while True:
                try:
                    text = self._stream.next()['text']
                    break
                except StopIteration:
                    time.sleep(0.1)
                    self._restart_stream()

            emoticons = self._find_emoticons(text)
            if len(emoticons) > 0:
                positive = np.random.choice(emoticons) in Emoticons.POSITIVE
                text_stripped = self._strip_emoticons(text)
                return text_stripped, emoticons, positive

class TweetEncoder(object):

    def __init__(self, text):
        self.chars = [''] + list(set(text))
        self.nchars = len(self.chars)
        self._c2i = {c:i for i,c in enumerate(self.chars)}

    def __call__(self, obj):
        if isinstance(obj, np.ndarray):
            if len(obj.shape) == 3:
                return self._decode_tweets(obj)
            elif len(obj.shape) == 2:
                return self._decode_tweet(obj)
        elif isinstance(obj, list):
            return self._encode_tweets(obj)
        elif isinstance(obj, unicode):
            return self._encode_tweet(obj)
        elif isinstance(obj, str):
            return self._encode_tweet(obj)
        else:
            raise ValueError

    def _encode_tweet(self, tweet):
        x = np.zeros((140, self.nchars))
        offset = 140 - len(tweet)
        for i, c in enumerate(tweet):
            j = self.c2i(c)
            x[i+offset, j] = 1
        return x

    def _encode_tweets(self, tweets):
        xs = [self._encode_tweet(t) for t in tweets]
        return np.stack(xs)

    def _decode_tweet(self, x):

        def choose_char(p):
            if np.sum(p) > 1e-6:
                p /= np.sum(p)
                return np.random.choice(self.chars, p=p)
            else:
                return ''

        chars = [choose_char(x[i,:]) for i in range(x.shape[0])]
        return ''.join(chars)

    def _decode_tweets(self, x):
        return [self._decode_tweet(x[i, :, :]) for i in range(x.shape[0])]

    def c2i(self, c):
        try:
            return self._c2i[c]
        except KeyError:
            return 0

class EmoticonEncoder(object):

    def __init__(self, emoticons=None):
        if emoticons is None:
            self._emoticons = Emoticons.POSITIVE + Emoticons.NEGATIVE
        else:
            self._emoticons = emoticons

        self._e2i = {e:i for i,e in enumerate(self._emoticons)}

    def _encode_emoticon(self, emos):
        x = np.zeros(len(self._emoticons))
        for e in emos:
            try:
                x[self._e2i[e]] = 1
            except KeyError:
                pass
        return x

    def _encode_emoticons(self, emos):
        return np.stack([self._encode_emoticon(e) for e in emos])

    def __call__(self, obj):

        if isinstance(obj, list):
            if isinstance(obj[0], list):
                return self._encode_emoticons(obj)
            elif isinstance(obj[0], str):
                return self._encode_emoticon(obj)
            elif isinstance(obj[0], unicode):
                return self._encode_emoticon(obj)

        raise ValueError
