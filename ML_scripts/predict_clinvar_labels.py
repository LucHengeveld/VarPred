import pickle
import pandas as pd
import numpy as np
import os
import sys

def load_ml_model(model_name):
    """Loads the ML model from a pickle

    Args:
        model_name: String with the name of the ML model

    Returns:
        The ML model
    """
    return pickle.load(open(model_name, "rb"))


def open_tsv_file(filename):
    """Opens a .tsv and parses it into a dataframe

    Args:
        filename: String of filename of the .tsv file

    Returns:
        Dataframe of the .tsv file
    """
    return pd.read_csv(filename, sep="\t")


def predict_labels(data):
    """Precticts the classes for the rows in the dataframe

    Args:
        data: Dataframe with clinvar data that gets classified

    Returns:
        Dataframe with the predticted classes,
        without the one hot encoding
    """
    subset = data.iloc[:, np.r_[5, 6, 7, 25, 27:31, 33:len(data.columns)]]
    prediction = model.predict(subset)
    prediction_proba = model.predict_proba(subset)
    proba_0 = list()
    proba_1 = list()
    for probability in prediction_proba:
        proba_0.append(probability[0])
        proba_1.append(probability[1])
    data["ML prediction"] = prediction
    data["Probability 0"] = proba_0
    data["Probability 1"] = proba_1
    return data.iloc[:, np.r_[0:32, -3, -2, -1]]


def write_file(data, filename):
    """Writes the dataframe to a .tsv file

    Args:
        data: Dataframe that gets written to dataframe
        filename: String of the filename
    """
    for column in data.columns:
        data[column]= data[column].map(str)
    data.to_json(filename, orient='records')


if __name__ == '__main__':
    file = sys.argv[1]
    model = load_ml_model("model.p")
    data = open_tsv_file("OHE_ClinVar_data.tsv")
    data = predict_labels(data)
    os.remove("OHE_ClinVar_data.tsv")
    f"{file}.p"
    write_file(data, f"variant-{file}.json")
