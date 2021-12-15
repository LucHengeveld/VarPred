import pickle
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, \
    precision_score, accuracy_score, \
    recall_score, roc_auc_score, roc_curve, f1_score
import os

# prepare the data
sns.set()

df = pd.read_csv('ML_data.tsv', sep='\t')

X = df.iloc[:, np.r_[5, 6, 7, 25, 27:31, 33:len(df.columns)]]
# X.to_csv("ML columns.tsv", sep="\t", index=False)

y = df['CLNSIG NUM']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20,
                                                    random_state=27)


def train_random_forest_classifier():
    """Trains the random forest classifier and pickles the trained model

    """
    # train model
    rfc = RandomForestClassifier(max_depth=10)
    rfc_model = rfc.fit(X_train, y_train)

    # calculate scores
    rfc_predict = rfc.predict(X_test)
    rfc_proba = rfc.predict_proba(X_test)
    results(rfc_predict, rfc_proba, y_test)

    # pickle model
    with open("model.p", "wb") as file:
        pickle.dump(rfc_model, file)


def results(prediction, prediction_proba, dataset):
    """Calculate and print accuracy, precision, Recall and F1 for given set

    Args:
        prediction: array containing predictions
        prediction_proba array containing probabilities
        dataset: array with y_test
    """
    print("\n _____ Results _____")
    print(f"Accuracy: {accuracy_score(dataset, prediction)}")
    print(f"Precision score: {precision_score(dataset, prediction)}")
    print(f"Recall score: {recall_score(dataset, prediction)}")
    print(f"F1-score: {f1_score(dataset, prediction)}")
    print(f"AUC score: {roc_auc_score(dataset, prediction_proba[:, 1])}")


if __name__ == '__main__':
    train_random_forest_classifier()
