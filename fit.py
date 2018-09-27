from app.ml import SentimentModel

sentiment_model = SentimentModel()

count = 0
while True:
    count += 1
    "\n\nTraining round: %i" % count
    sentiment_model.fit(steps_per_epoch=1e2, nb_epoch=10, save=True)
