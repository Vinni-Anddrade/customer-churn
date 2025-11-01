import pandas as pd


class DataReader:
    def __init__(self, path):
        self.path = path

    def read_data_from_csv(self):
        df = pd.read_csv(self.path, sep=",")
        df["TotalCharges"] = df["TotalCharges"].apply(
            lambda x: None if x == " " else float(x)
        )

        df["Tenure"] = df["Tenure"].astype("int")
        df["MonthlyCharges"] = df["MonthlyCharges"].astype("float")
        df["TotalCharges"] = df["TotalCharges"].astype("float")

        df = df.loc[~df["TotalCharges"].isna()]

        return df
