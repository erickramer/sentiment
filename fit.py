from app.ml import SentimentModel

sentiment_model = SentimentModel()

count = 0
while True:
    count += 1
    "\n\nTraining round: %i" % count
    sentiment_model.fit(samples_per_epoch=1e4, nb_epoch=10)
