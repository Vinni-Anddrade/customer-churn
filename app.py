from flask import Flask, render_template
import requests
from flask_cors import CORS


payload = {
    "records": [
        {
            "customerID": "8773-RKXTP",
            "Gender": "Female",
            "SeniorCitizen": 0,
            "Partner": "No",
            "Dependents": "No",
            "Tenure": 35,
            "PhoneService": "Yes",
            "MultipleLines": "No",
            "InternetService": "DSL",
            "OnlineSecurity": "Yes",
            "OnlineBackup": "No",
            "DeviceProtection": "No",
            "TechSupport": "No",
            "StreamingTV": "No",
            "StreamingMovies": "No",
            "Contract": "One year",
            "PaperlessBilling": "No",
            "PaymentMethod": "Manual",
            "MonthlyCharges": 54.85,
            "TotalCharges": 1934.5,
        },
        {
            "customerID": "1374-KVMWE",
            "Gender": "Male",
            "SeniorCitizen": 0,
            "Partner": "Yes",
            "Dependents": "No",
            "Tenure": 2,
            "PhoneService": "Yes",
            "MultipleLines": "No",
            "InternetService": "Fiber optic",
            "OnlineSecurity": "No",
            "OnlineBackup": "No",
            "DeviceProtection": "Yes",
            "TechSupport": "No",
            "StreamingTV": "Yes",
            "StreamingMovies": "No",
            "Contract": "Monthly",
            "PaperlessBilling": "Yes",
            "PaymentMethod": "Manual",
            "MonthlyCharges": 69.7,
            "TotalCharges": 118.9,
        },
        {
            "customerID": "7392-BMMED",
            "Gender": "Female",
            "SeniorCitizen": 1,
            "Partner": "No",
            "Dependents": "No",
            "Tenure": 56,
            "PhoneService": "No",
            "MultipleLines": "No",
            "InternetService": "DSL",
            "OnlineSecurity": "Yes",
            "OnlineBackup": "Yes",
            "DeviceProtection": "Yes",
            "TechSupport": "Yes",
            "StreamingTV": "No",
            "StreamingMovies": "No",
            "Contract": "One year",
            "PaperlessBilling": "No",
            "PaymentMethod": "Bank transfer (automatic)",
            "MonthlyCharges": 42.3,
            "TotalCharges": 2341.9,
        },
        {
            "customerID": "3549-NHRJG",
            "Gender": "Male",
            "SeniorCitizen": 0,
            "Partner": "Yes",
            "Dependents": "No",
            "Tenure": 3,
            "PhoneService": "Yes",
            "MultipleLines": "Yes",
            "InternetService": "DSL",
            "OnlineSecurity": "No",
            "OnlineBackup": "Yes",
            "DeviceProtection": "No",
            "TechSupport": "No",
            "StreamingTV": "Yes",
            "StreamingMovies": "No",
            "Contract": "Monthly",
            "PaperlessBilling": "Yes",
            "PaymentMethod": "Manual",
            "MonthlyCharges": 63.5,
            "TotalCharges": 195.6,
        },
        {
            "customerID": "6984-YZZOT",
            "Gender": "Female",
            "SeniorCitizen": 1,
            "Partner": "No",
            "Dependents": "No",
            "Tenure": 70,
            "PhoneService": "Yes",
            "MultipleLines": "No",
            "InternetService": "DSL",
            "OnlineSecurity": "Yes",
            "OnlineBackup": "Yes",
            "DeviceProtection": "No",
            "TechSupport": "No",
            "StreamingTV": "No",
            "StreamingMovies": "No",
            "Contract": "Two year",
            "PaperlessBilling": "No",
            "PaymentMethod": "Credit card (automatic)",
            "MonthlyCharges": 56.9,
            "TotalCharges": 3880.7,
        },
    ]
}


app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/model_result", methods=["GET", "POST"])
def model_result():
    url = "http://127.0.0.1:5050/execute_model"
    response = requests.post(url=url, json=payload)
    data = response.json()

    results = data.get("results", [])

    headers = results[0].keys() if results else []
    return render_template("model_result.html", headers=headers, results=results)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8085, debug=True)
