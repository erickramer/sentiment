import keras
from keras.models import Model
from keras.layers import Input
from keras.layers.core import Dense, Dropout
from keras.layers.embeddings import Embedding
from keras.layers.recurrent import LSTM

from app import db, app
from app.emojis import emojis
from app.models import Tweet

import os
import numpy as np

def data_gen(batch_size=100):
    # loading all tweets into memory for speed
    tweets = db.session.query(Tweet).all()

    xs = []
    ys = []
    ss = []

    while True:
        np.random.shuffle(tweets)

        for tweet in tweets:
            xs.append(tweet.x)
            ys.append(tweet.y)
            ss.append(tweet.sentiment)

            if len(xs) == batch_size:
                yield np.stack(xs), [np.stack(ys), np.stack(ss)]
                xs = []
                ys = []
                ss = []

class SentimentModel(object):

    def __init__(self, model = None):
        if model is None:
            if os.path.exists(self.model_path):
                self._model = self._load_model()
            else:
                self._model = self._build_model()
        else:
            self._model = model

    @property
    def _baseline(self):
        tweet = Tweet("")
        x = tweet.x.reshape(1, -1)
        scores, sentiment = self._model.predict(x)
        return scores

    @property
    def model_path(self):
        return os.path.join(app.config['BASE_DIR'], 'data/model.h5')

    def _build_model(self):
        text = Input(shape=(140,))

        x = Embedding(input_dim=5000, output_dim=64)(text)
        x = LSTM(128)(x)
        x = Dropout(0.5)(x)

        emoji = Dense(len(emojis), activation="sigmoid", name="emoji")(x)
        sentiment = Dense(3, activation="sigmoid", name="sentiment")(x)

        model = Model(text, [emoji, sentiment])

        model.compile("RMSprop",
                  loss={'sentiment': "binary_crossentropy", "emoji": "binary_crossentropy"},
                  loss_weights={"sentiment":0.5, "emoji": 0.5})

        return model

    def _load_model(self):
        return keras.models.load_model(self.model_path)

    def fit(self, batch_size=100, samples_per_epoch=1e3,
            nb_epoch=10, save=True):

        gen = data_gen(batch_size)

        self._model.fit_generator(gen,
                samples_per_epoch=samples_per_epoch,
                nb_epoch=nb_epoch)

        if save:
            self._model.save(self.model_path)

    def score(self, text):
        tweet = Tweet(text)
        x = tweet.x.reshape(1, -1)
        scores, sentiment = self._model.predict(x)

        scores /= self._baseline
        scores = [float(s) for s in scores[0, :]]
        scores = dict(zip(emojis, scores))
        sentiment = float(sentiment[0, 0])
        return {"emoji":scores, "sentiment": sentiment}
