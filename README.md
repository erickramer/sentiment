# Twitter Emoji Sentiment

This WebApp tags text with possible emojis. On the backend, I'm using a neural
network with an [LSTM layer from Keras](https://keras.io/layers/recurrent/). On
the frontend, I'm using [D3](https://d3js.org/) and jQuery to animate the barplots.

The training data comes from twitter using [python-twitter](https://github.com/bear/python-twitter)'s
streaming API. The ```add_tweets.py``` script streams tweets with emojis into a SQLite database for
training. The ```fit.py``` script trains the neural network and saves the output
to ```data/model.5h```


## Install

1) Clone the repo

```
git clone https://github.com/erickramer/sentiment.git
cd sentiment
```

2) Create virtualenv and install packages

```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

3) Run WebApp

```
python run_app.py
```

Now you have the WebApp running at [localhost:5000](localhost:5000)

## Streaming Tweets (optional)

If you want to add tweets to the SQLite database, do the following:

1) Create ```config.py``` in the base directory

This file should look like this:

```
consumer_key = 'YOUR CONSUMER KEY'
consumer_secret = 'YOUR CONSUMER SECRET'
access_token = 'YOUR ACCESS TOKEN'
access_token_secret = 'YOUR ACCESS TOKEN SECRET'
```

2) Run ```python add_tweets.py```

## Fitting model (optional)

If you want to train the model for additional epochs to get a better fit, do the following

It helps if you have a GPU

1) Run ```python fit.py```
