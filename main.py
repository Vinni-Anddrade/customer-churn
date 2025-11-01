from src.inference import get_data, get_production_model
from flask import Flask, request, jsonify
import pandas as pd
from src.components.data_reader import DataReader
from src.components.data_treatment import DataTreatment
import os
from pathlib import Path


app = Flask(__name__)


def main(data):
    # predict_df = get_data() # Reading data from our csv folder
    predict_df = pd.DataFrame(data["records"])  # Getting data from postman
    model, model_name = get_production_model()

    treatment_manager = DataTreatment(predict_df, model_name)
    breakpoint()
    result = [str(i) for i in model.predict(treatment_manager.df)]

    predict_df["ChurnPrediction"] = result
    predict_df.rename(columns={"customerID": "CustomerID"}, inplace=True)

    json_output = predict_df.to_dict(orient="records")
    json_output = {"records": json_output}

    return jsonify(json_output)


@app.route("/")
def home():
    return "To execute the model, go to route: /execute_model with the data"


@app.route("/execute_model", methods=["POST"])
def model_execution():
    data = request.get_json()
    output_model = main(data)
    return output_model


if __name__ == "__main__":
    app.run(port=5050, debug=True)
