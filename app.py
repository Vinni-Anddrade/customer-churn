from flask import Flask, render_template
from flask_cors import CORS
import os
from pathlib import Path
import requests
import time

from src.components.data_reader import DataReader


def wait_for_api(url, timeout=30):
    start_time = time.time()
    while True:
        try:
            response = requests.get(url)
            if response.status_code < 500:
                print(f"API {url} está pronta!")
                return True
        except requests.exceptions.RequestException:
            pass
        if time.time() - start_time > timeout:
            print(f"Timeout! API {url} não respondeu em {timeout} segundos.")
            return False
        print("Esperando API ficar pronta...")
        time.sleep(2)


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

API_URL = os.getenv("API_URL", "http://main:5050")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/model_result", methods=["GET", "POST"])
def model_result():
    payload = main()
    response = requests.post(url=f"{API_URL}/execute_model", json=payload)
    data = response.json()
    results = data.get("records", [])

    headers = results[0].keys() if results else []
    return render_template("model_result.html", headers=headers, results=results)


if __name__ == "__main__":
    wait_for_api(f"{API_URL}/execute_model")
    app.run(host="0.0.0.0", port=8085)
