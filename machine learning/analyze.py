import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.core.base import DataError
import seaborn as sns
import pandas as pd
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import roc_curve
from sklearn.metrics import auc
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression, MultiTaskLasso
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from mlxtend.plotting import plot_confusion_matrix

sns.set()

# age;sex;cp;trestbps;chol;fbs;restecg;thalach;exang;oldpeak;slope;ca;thal;target'
df = pd.read_csv('heart.csv', sep=';')
print(df.columns)
print("Number of patients: " + str(len(df.index)-1))
print("Number of diseased: " + str(df['target'].value_counts()[1]))
print("Number of males: " + str(df['sex'].value_counts()[1]))
print("Number of females: " + str(df['sex'].value_counts()[0]))
X = df.iloc[:,:-1]
y = df['target']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=27)
#plt.hist(df['age'])
#plt.show()
SVC_model = SVC()
# KNN model requires you to specify n_neighbors,
# the number of points the classifier will look at to determine what class a new point belongs to
KNN_model = KNeighborsClassifier(n_neighbors=6)
Logistic_regression_model = LogisticRegression()
lda = LinearDiscriminantAnalysis()
clf = DecisionTreeClassifier()
rfc = RandomForestClassifier()
mtl = MultiTaskLasso()

##mtl.fit(X_train, y_train)
SVC_model.fit(X_train, y_train)
KNN_model.fit(X_train, y_train)
Logistic_regression_model.fit(X_train, y_train)
lda.fit(X_train, y_train)
clf_model = clf.fit(X_train, y_train)
rfc_model = rfc.fit(X_train, y_train)
#print(vars(Logistic_regression_model))
SVC_prediction = SVC_model.predict(X_test)
KNN_prediction = KNN_model.predict(X_test)
Logistic_regression_prediction = Logistic_regression_model.predict(X_test)
lda_prediction = lda.predict(X_test)
lda_pred_proba = lda.predict_proba(X_test)[:, 1]
clf_prediction = clf_model.predict(X_test)
rfc_prediction = rfc_model.predict(X_test)
#mtl_prediction = mtl.predict(X_test)


cm = confusion_matrix(y_test, lda_prediction)
tn, fp, fn, tp = confusion_matrix(y_test, lda_prediction).ravel()
print("FPR: " + str(fp / (fp + tn)))
print("FNR: " + str(fn / (fn + tp)))
print("Specificity: " + str(tn / (fp + tn)))
print("Sensitivity: " + str(tp / (tp + fn)))
fig, ax = plot_confusion_matrix(conf_mat=cm)
plt.rcParams['font.size'] = 20
plt.title("LDA")
plt.show()

[fpr, tpr, thr] = roc_curve(y_test, lda_pred_proba)
idx = np.min(np.where(tpr > 0.95)) 
plt.figure(figsize=(10, 10))
plt.plot(fpr, tpr, color='coral', label='ROC curve (area = %0.3f)' % auc(fpr, tpr))
plt.plot([0, 1], [0, 1], 'k--')
plt.plot([0, fpr[idx]], [tpr[idx], tpr[idx]], 'k--')
plt.plot([fpr[idx], fpr[idx]], [0, tpr[idx]], 'k--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate (1 - specificity)', fontsize=10)
plt.ylabel('True Positive Rate (recall)', fontsize=10)
plt.title('lda Receiver operating characteristic (ROC) curve')
plt.legend(loc="lower right")
plt.show()

print(accuracy_score(SVC_prediction, y_test))
print(accuracy_score(KNN_prediction, y_test))
print(accuracy_score(Logistic_regression_prediction, y_test))
print(accuracy_score(lda_prediction, y_test))
print(accuracy_score(clf_prediction, y_test))
print(accuracy_score(rfc_prediction, y_test))
