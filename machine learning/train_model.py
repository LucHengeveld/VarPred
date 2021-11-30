import pickle
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# prepare the data
sns.set()

df = pd.read_csv('ML data.tsv', sep='\t')

X = df.iloc[:, np.r_[5, 6, 7, 25, 27:31, 33:len(df.columns)]]
X.to_csv("ML columns.tsv", sep="\t", index=False)
# print(X)

y = df['CLNSIG NUM']
# print(y)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20,
                                                    random_state=27)


def train_random_forest_classifier():
    """Trains the random forest classifier and pickles the trained model

    """
    rfc = RandomForestClassifier(max_depth=10)
    rfc_model = rfc.fit(X_train, y_train)
    with open("model.p", "wb") as file:
        pickle.dump(rfc_model, file)


if __name__ == '__main__':
    train_random_forest_classifier()
