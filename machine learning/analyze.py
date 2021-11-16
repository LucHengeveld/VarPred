from pandas.core.base import DataError
import seaborn as sns
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from make_plots import makeplots
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import roc_curve
from sklearn.metrics import auc
from mlxtend.plotting import plot_confusion_matrix
import matplotlib.pyplot as plt
import numpy as np

sns.set()

# age;sex;cp;trestbps;chol;fbs;restecg;thalach;exang;oldpeak;slope;ca;thal;target'
df = pd.read_csv('ML data.tsv', sep='\t')
df.to_csv("test.tsv", sep="\t")
X = df.iloc[:, np.r_[2, 5, 6, 7, 25, 27, 28, 31:len(df.columns)]]
X.to_csv("test.tsv", sep="\t")
y = df['CLNSIG NUM']
print(y)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20,
                                                    random_state=27)


# Linear Discriminant analysis
#
#
lda = RandomForestClassifier()
lda.fit(X_train, y_train)
lda_prediction = lda.predict(X_test)
lda_pred_proba = lda.predict_proba(X_test)[:, 1]
# makeplots(lda_prediction,lda_pred_proba, y_test)
cm = confusion_matrix(y_test, lda_prediction)
list_ding = list(confusion_matrix(y_test, lda_prediction).ravel())
for importance, name in sorted(zip(lda.feature_importances_, X_train.columns),
                               reverse=True):
    print(name, importance)
print(accuracy_score(lda_prediction, y_test))

# print("FPR: " + str(fp / (fp + tn)))
# print("FNR: " + str(fn / (fn + tp)))
# print("Specificity: " + str(tn / (fp + tn)))
# print("Sensitivity: " + str(tp / (tp + fn)))
fig, ax = plot_confusion_matrix(conf_mat=cm)
plt.rcParams['font.size'] = 20
plt.title("LDA")
plt.show()
# Decision tree classifier
#
#
# clf = DecisionTreeClassifier()
# clf_model = clf.fit(X_train, y_train)
# clf_prediction = clf_model.predict(X_test)
#
# # Random tree classifier
# #
# #
# rfc = RandomForestClassifier()
# rfc_model = rfc.fit(X_train, y_train)
# rfc_prediction = rfc_model.predict(X_test)
#
# # Logistic regression
# #
# #
# Logistic_regression_model = LogisticRegression()
# Logistic_regression_model.fit(X_train, y_train)
# Logistic_regression_prediction = Logistic_regression_model.predict(X_test)
