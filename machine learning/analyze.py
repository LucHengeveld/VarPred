import pandas as pd
import numpy as np
from pandas.core.base import DataError
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from make_plots import makeplots

sns.set()

df = pd.read_csv('ML data.tsv', sep='\t')

X = df.iloc[:, np.r_[27,28, 31:len(df.columns)]]
y = df['CLNSIG NUM']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=27)


# Linear Discriminant analysis
#
#
lda = LinearDiscriminantAnalysis()
lda.fit(X_train, y_train)
lda_prediction = lda.predict(X_test)
lda_pred_proba = lda.predict_proba(X_test)[:, 1]
#makeplots(lda_prediction,lda_pred_proba, y_test)

# Decision tree classifier
#
#
clf = DecisionTreeClassifier()
clf_model = clf.fit(X_train, y_train)
clf_prediction = clf_model.predict(X_test)
clf_pred_proba = clf.predict_proba(X_test)[:, 1]
#makeplots(clf_prediction, clf_pred_proba, y_test)

# Random tree classifier
#
#
rfc = RandomForestClassifier()
rfc_model = rfc.fit(X_train, y_train)
rfc_prediction = rfc_model.predict(X_test)

# Logistic regression
#
#
Logistic_regression_model = LogisticRegression(max_iter=5000)
Logistic_regression_model.fit(X_train, y_train)
Logistic_regression_prediction = Logistic_regression_model.predict(X_test)
Logistic_regression_pred_proba = Logistic_regression_model.predict_proba(X_test)
makeplots(Logistic_regression_prediction, Logistic_regression_pred_proba, y_test)