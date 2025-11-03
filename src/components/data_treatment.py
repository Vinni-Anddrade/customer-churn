import pandas as pd
from sklearn.preprocessing import StandardScaler

from src.utils.utils import read_yaml


class DataTreatment:
    def __init__(self, df: pd.DataFrame, model_name: str):
        self.df = df
        self.model_name = model_name
        breakpoint()
        self.data_configuration()
        self.make_one_hot_encoding()
        self.check_columns(self.columns)
        # Here I'll reorder the cols to match the model's schema
        self.df = self.df.loc[:, self.columns]
        # self.df = self.drop_cols()
        # dp_models = ["Deep Learning"]

        # if self.model_name.split("_")[0] in dp_models:
        #     self.df = self.standardize_data()

    def data_configuration(self):
        config_path = "./src/config/schema.yaml"
        schema_file = read_yaml(config_path)
        self.columns = schema_file["columns"]

        self.df = self.df.drop(["customerID"], axis=1)

    def make_one_hot_encoding(self):
        self.df = pd.get_dummies(data=self.df, dtype="int")

    def check_columns(self, original_schema: list):
        new_df_columns = self.df.columns

        for col in original_schema:
            if col not in new_df_columns:
                self.df[col] = 0

    def drop_cols(self):
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

        return self.df.drop(cols_to_drop, axis=1)

    def standardize_data(self):
        scaler = StandardScaler().fit(self.df)
        return scaler.transform(self.df)
