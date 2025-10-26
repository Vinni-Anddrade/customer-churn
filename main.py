from src.inference import get_data, get_production_model, data_treatment


def main():
    predict_df = get_data()

    model, model_name = get_production_model()
    df_treated = data_treatment(predict_df, model_name)

    result = model.predict(df_treated)

    print(result)


if __name__ == "__main__":
    main()
