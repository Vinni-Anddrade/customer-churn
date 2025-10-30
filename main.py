from src.inference import get_data, get_production_model, data_treatment
from flask import Flask, request, jsonify
import pandas as pd


app = Flask(__name__)


def main(data):
    # predict_df = get_data() # Reading data from our csv folder
    predict_df = pd.DataFrame(data["records"])  # Getting data from postman

    model, model_name = get_production_model()
    df_treated = data_treatment(predict_df, model_name)

    result = [str(i) for i in model.predict(df_treated)]
    indexation = [str(i) for i in range(1, len(result) + 1)]
    output_dict = dict(zip(indexation, result))
    json_output = {"results": [output_dict]}

    return jsonify(json_output)


@app.route("/")
def home():
    return "To execute the model, go to route: /execute_model with the data"


@app.route("/execute_model", methods=["POST"])
def model_execution():
    data = request.get_json()
    output_api = main(data)

    return output_api


if __name__ == "__main__":
    app.run(port=5050, debug=True)
