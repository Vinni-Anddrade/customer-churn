import pandas as pd
import mlflow
from mlflow import MlflowClient


def get_data():
    path = "./data/new_customer_analysis.csv"
    df = pd.read_csv(path, header=0, sep=";")

    return df


def check_production_model():
    mlflow.set_tracking_uri("http://host.docker.internal:5000")
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

    mlflow.set_tracking_uri("http://host.docker.internal:5000")
    model_uri = f"models:/{model_name}@prod"
    try:
        model = mlflow.pyfunc.load_model(model_uri=model_uri)
        return model, model_name

    except Exception as e:
        print(e)
        print("No model was found in production.")
        return None
