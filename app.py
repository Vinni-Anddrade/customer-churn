from flask import Flask, render_template
import requests
from flask_cors import CORS
import os
from pathlib import Path
from src.components.data_reader import DataReader


def main():
    PATH = Path().resolve()
    file_path = os.path.join(PATH, "data", "new_customer_analysis.csv")
    reader_manager = DataReader(file_path)
    predict_df = reader_manager.read_data_from_csv()
    json_output = predict_df.to_dict(orient="records")
    json_output = {"records": json_output}

    return json_output


app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/model_result", methods=["GET", "POST"])
def model_result():
    payload = main()
    url = "http://127.0.0.1:5050/execute_model"
    response = requests.post(url=url, json=payload)
    data = response.json()
    results = data.get("records", [])

    headers = results[0].keys() if results else []
    return render_template("model_result.html", headers=headers, results=results)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8085, debug=True)
