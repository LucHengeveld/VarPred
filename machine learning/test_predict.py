import pickle
import pandas as pd
import numpy as np


if __name__ == '__main__':
    model = pickle.load(open("model.p", "rb"))

    data = pd.read_csv("testbestand.tsv", sep="\t")
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
    data = data.iloc[:, np.r_[0:32, -3, -2, -1]]
    data.to_csv("testbestand2.tsv", sep="\t", index=False)
