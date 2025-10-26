import pandas as pd
import mlflow
from mlflow import MlflowClient
from sklearn.preprocessing import StandardScaler
from utils.utils import read_yaml


def get_data():
    path = "../data/new_customer_analysis.csv"
    breakpoint()
    df = pd.read_csv(path, header=0, sep=";")

    return df


def data_treatment(df: pd.DataFrame, model_name):
    config_path = "./config/schema.yaml"
    schema_file = read_yaml(config_path)
    columns = schema_file["columns"]

    df = df.drop(["customerID"], axis=1)

    def drop_cols(df: pd.DataFrame):
        cols_to_drop = [
            "SeniorCitizen",
            "MultipleLines_No",
            "InternetService_DSL",
            "OnlineSecurity_No",
            "OnlineBackup_No",
            "DeviceProtection_No",
            "TechSupport_No",
            "StreamingMovies_No",
            "Contract_Monthly",
        ]

        return df.drop(cols_to_drop, axis=1)

    def make_one_hot_encoding(df: pd.DataFrame):
        return pd.get_dummies(data=df, dtype="int")

    def check_columns(df: pd.DataFrame, original_schema: list):
        new_df_columns = df.columns

        for col in original_schema:
            if col not in new_df_columns:
                df[col] = 0

        return df

    def standardize_data(df: pd.DataFrame):
        scaler = StandardScaler().fit(df)
        return scaler.transform(df)

    breakpoint()
    df = make_one_hot_encoding(df)
    df = check_columns(df, columns)
    df = drop_cols(df)
    dp_models = ["Deep Learning"]

    if model_name.split("_")[0] in dp_models:
        df = standardize_data(df)

    return df


def check_production_model():
    mlflow.set_tracking_uri("http://localhost:5000")
    client = MlflowClient()
    registered_models = client.search_registered_models()

    production_models = list()

    for model in registered_models:
        model_name = model.name
        aliases = [i for i in model.aliases.keys()]
        if len(aliases) > 0:
            stage = aliases[0]

            if stage == "prod":
                production_models.append(model_name)

    return production_models[0]


def get_production_model():

    model_name = check_production_model()

    mlflow.set_tracking_uri("http://localhost:5000")
    model_uri = f"models:/{model_name}@prod"
    try:
        model = mlflow.pyfunc.load_model(model_uri=model_uri)
        return model, model_name

    except Exception as e:
        print(e)
        print("No model was found in production.")
        return None


if __name__ == "__main__":

    predict_df = get_data()

    model, model_name = get_production_model()
    df_treated = data_treatment(predict_df, model_name)

    result = model.predict(df_treated)

    print(result)
