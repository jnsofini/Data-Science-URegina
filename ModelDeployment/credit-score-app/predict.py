""" 
Deployment of app with flash.
"""
import json
import os

import pandas as pd
from flask import Flask, jsonify, request
from optbinning import Scorecard


# Makes sure the data is preprocess in way to conform to what
# the app expects
def load_model():
    print("Loading Model=================================")
    model_location = os.getenv("MODEL_LOCATION", "model")
    model = Scorecard.load(f"{model_location}/model.pkl")
    return model


class ModelService:
    def __init__(self, model, model_version=None, callbacks=None):
        self.model = model
        self.model_version = model_version
        self.callbacks = callbacks or []

    def prepare_features(self, record):
        return pd.DataFrame([record])

    def predict(self, features):
        score = self.model.score(features)
        return int(score[0])

    def score_events(self, record):
        print(json.dumps(record))

        predictions_events = []

        cust = record["cust"]
        cust_id = record["cust_id"]
        features = self.prepare_features(cust)
        prediction = self.predict(features)

        prediction_event = {
            "model": "risk_score_model",
            "version": self.model_version,
            "prediction": {"cust_score": prediction, "cust_id": cust_id},
        }
        for callback in self.callbacks:
            callback(prediction_event)

        predictions_events.append(prediction_event)

        return {"predictions": predictions_events}


# Start a flask application to make the script run as flast server
app = Flask("credit-score-prediction")
model = load_model()
model_service = ModelService(model=model, model_version="V1")


@app.route("/predict", methods=["POST"])
def predict_endpoint():
    customer = (
        request.get_json()
    )  # Flask function don't take params, they can be gotten from request

    # features = model_service.prepare_features(customer)
    # pred = model_service.predict(features)

    result = model_service.score_events(record=customer)

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=9696)  # Debugging server only
