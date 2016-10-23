from app import app, db
from emojis import *
import numpy as np

class Tweet(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    raw_tweet = db.Column(db.String(140))

    def __init__(self, raw_tweet):
        self.raw_tweet = raw_tweet

    @property
    def text(self):
        text = self.raw_tweet
        for e in emojis:
            text = text.replace(e, "")
        return text

    @property
    def emojis(self):
        return [e for e in emojis if e in self.raw_tweet]

    @property
    def sentiment(self):
        x = np.zeros(3)
        if len(self.emojis) > 0:
            e = np.random.choice(self.emojis)
            if e in positive_emojis:
                x[0] = 1
                return x
            elif e in negative_emojis:
                x[2] = 1
                return x
            else:
                x[1] = 1
                return x
        return x

    @property
    def x(self):
        # left-pad with zeros
        x = []
        if len(self.text) < 140:
            x += [0] * (140 - len(self.text))
        x += [ord(c) % 5000 for c in self.text]
        return np.array(x[0:140])

    @property
    def y(self):
        y = np.zeros(len(emojis))
        for e in self.emojis:
            y[emojis.index(e)] = 1
        return y
