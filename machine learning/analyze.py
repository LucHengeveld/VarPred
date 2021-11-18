import numpy as np
import seaborn as sns
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, precision_score, accuracy_score, recall_score, roc_auc_score, \
    roc_curve, f1_score
from mlxtend.plotting import plot_confusion_matrix
from matplotlib import pyplot as plt
from sklearn.tree import DecisionTreeClassifier

# Prepare the data data

sns.set()


df = pd.read_csv('ML data.tsv', sep='\t')

X = df.iloc[:, np.r_[5, 6, 7, 25, 27:31, 33:len(df.columns)]]
# print(X)

# X = df.iloc[:, np.r_[27, 28, 31:len(df.colums)]]
y = df['CLNSIG NUM']
# print(y)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20,
                                                    random_state=27)


def lda():
    print("##### Linear discriminant analysis #####")
    lda = LinearDiscriminantAnalysis()
    lda.fit(X_train, y_train)
    lda_prediction = lda.predict(X_test)
    lda_prediction_proba = lda.predict_proba(X_test)
    cm = confusion_matrix(y_test, lda_prediction)
    # list_lda = list(confusion_matrix(y_test, lda_prediction).ravel())
    for importance, name in sorted(zip(lda.coef_[0], X_train.columns),
                                   reverse=True):
        print(name, importance)

    results(lda_prediction, lda_prediction_proba)
    plot_matrix(cm, "Linear discriminant analysis")
    plot_auc(lda_prediction_proba, "linear discriminant analysis")


def decision_tree():
    print("##### Decision tree #####")
    clf = DecisionTreeClassifier()
    clf_model = clf.fit(X_train, y_train)
    clf_prediction = clf_model.predict(X_test)
    clf_prediction_proba = clf.predict_proba(X_test)
    cm = confusion_matrix(y_test, clf_prediction)
    # lijst_decision = list(confusion_matrix(y_test, clf_prediction).ravel())
    for importance, name in sorted(zip(clf.feature_importances_, X_train.columns),
                                   reverse=True):
        print(name, importance)

    results(clf_prediction, clf_prediction_proba)
    plot_matrix(cm, "Decision tree")
    plot_auc(clf_prediction_proba, "decision tree")


def random_forest():
    print("##### Random forest #####")
    rfc = RandomForestClassifier()
    rfc_model = rfc.fit(X_train, y_train)
    rfc_prediction = rfc_model.predict(X_test)
    rfc_prediction_proba = rfc.predict_proba(X_test)
    cm = confusion_matrix(y_test, rfc_prediction)
    # lijst_random = list(confusion_matrix(y_test, rfc_prediction).ravel())

    for importance, name in sorted(zip(rfc.feature_importances_, X_train.columns),
                                   reverse=True):
        print(name, importance)

    results(rfc_prediction, rfc_prediction_proba)
    plot_matrix(cm, "Random forest")
    plot_auc(rfc_prediction_proba, "random forest")


def logistic():
    print("##### Logistic regression #####")
    logistic_regression_model = LogisticRegression()
    logistic_regression_model.fit(X_train, y_train)
    logistic_regression_prediction = logistic_regression_model.predict(X_test)
    lrm_prediction_proba = logistic_regression_model.predict_proba(X_test)
    cm = confusion_matrix(y_test, logistic_regression_prediction)
    # list_logistic = list(confusion_matrix(y_test, logistic_regression_prediction).ravel())

    for importance, name in sorted(zip(logistic_regression_model.coef_[0], X_train.columns),
                                   reverse=True):
        print(name, importance)

    results(logistic_regression_prediction, lrm_prediction_proba)
    plot_matrix(cm, "Logistic regression")
    plot_auc(lrm_prediction_proba, "logistic regression")


def plot_matrix(cm, name):
    display_labels = ["Benign", "Likely benign", "drug response", "Likely pathogenic", "Pathogenic"]
    fig, ax = plt.subplots(figsize=(6, 6))
    plot_confusion_matrix(conf_mat=cm, axis=ax)
    ax.set_xticklabels([''] + display_labels, rotation=45)
    ax.set_yticklabels([''] + display_labels)
    plt.rcParams['font.size'] = 20
    plt.title(f"Confusion matrix {name}")
    plt.subplots_adjust(bottom=0.25)
    plt.subplots_adjust(left=0.25)
    plt.show()


def plot_auc(prediction_proba, name):
    fpr = {}
    tpr = {}
    thresh = {}
    n_class = 5

    for i in range(n_class):
        fpr[i], tpr[i], thresh[i] = roc_curve(y_test, prediction_proba[:, i], pos_label=i)

    plt.plot(fpr[0], tpr[0], linestyle='--', color='orange', label='Benign')
    plt.plot(fpr[1], tpr[1], linestyle='--', color='green', label='Likely benign')
    plt.plot(fpr[2], tpr[2], linestyle='--', color='blue', label='drug response')
    plt.plot(fpr[3], tpr[3], linestyle='--', color='red', label='Likely pathogenic')
    plt.plot(fpr[4], tpr[4], linestyle='--', color='purple', label='Pathogenic')
    plt.plot([0, 1], [0, 1], 'k--')
    plt.title(f'Multiclass ROC curve {name}')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive rate')
    plt.legend(loc='best')
    plt.show()


def results(prediction, prediction_proba):
    print(f"\n _____ Results _____")
    print(f"Accuracy: {accuracy_score(y_test, prediction)}")
    print(f"Precision score: {precision_score(y_test, prediction, average='weighted')}")
    print(f"Recall score: {recall_score(y_test, prediction, average='weighted')}")
    print(f"F1-score: {f1_score(y_test, prediction, average='weighted')}")
    print(f"AUC score: {roc_auc_score(y_test, prediction_proba, average='weighted', multi_class='ovr')}")


def main():
    # lda()
    # decision_tree()
    random_forest()
    # logistic()


main()
