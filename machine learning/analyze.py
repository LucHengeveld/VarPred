import numpy as np
import seaborn as sns
import pandas as pd
from seaborn.utils import load_dataset
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, precision_score, accuracy_score, \
    recall_score, roc_auc_score, roc_curve, f1_score
from mlxtend.plotting import plot_confusion_matrix
from matplotlib import pyplot as plt
from sklearn.tree import DecisionTreeClassifier

# Prepare the data data

sns.set()

df = pd.read_csv('ML data.tsv', sep='\t')

X = df.iloc[:, np.r_[5, 6, 7, 25, 27:31, 33:77]]
# print(X)

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
    clf = DecisionTreeClassifier(max_depth=10)
    clf_model = clf.fit(X_train, y_train)
    clf_prediction = clf_model.predict(X_test)
    clf_prediction_proba = clf.predict_proba(X_test)
    cm = confusion_matrix(y_test, clf_prediction)
    # lijst_decision = list(confusion_matrix(y_test, clf_prediction).ravel())
    count = 0
    for importance, name in sorted(
            zip(clf.feature_importances_, X_train.columns),
            reverse=True):
        print(name, importance)

    results(clf_prediction, clf_prediction_proba)
    plot_matrix(cm, "Decision tree")
    plot_auc(clf_prediction_proba, "decision tree")


def random_forest_train():
    print("##### Random forest #####")
    rfc = RandomForestClassifier(max_depth=10)
    rfc_model = rfc.fit(X_train, y_train)
    rfc_prediction = rfc_model.predict(X_train)
    rfc_prediction_proba = rfc.predict_proba(X_train)
    cm = confusion_matrix(y_train, rfc_prediction)
    # lijst_random = list(confusion_matrix(y_test, rfc_prediction).ravel())

    for importance, name in sorted(zip(rfc.feature_importances_, X_train.columns),
                                   reverse=True)[:10]:
        print(name, importance)

    results(rfc_prediction, rfc_prediction_proba, y_train)
    plot_matrix(cm, "Random forest")
    plot_auc(rfc_prediction_proba, "random forest")

def random_forest_test():
    print("##### Random forest #####")
    rfc = RandomForestClassifier(max_depth=10)
    rfc_model = rfc.fit(X_train, y_train)
    rfc_prediction = rfc_model.predict(X_test)
    rfc_prediction_proba = rfc.predict_proba(X_test)
    cm = confusion_matrix(y_test, rfc_prediction)
    # lijst_random = list(confusion_matrix(y_test, rfc_prediction).ravel())

    for importance, name in sorted(
            zip(rfc.feature_importances_, X_train.columns),
            reverse=True)[:10]:
        print(name, importance)

    results(rfc_prediction, rfc_prediction_proba, y_test)
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

    for importance, name in sorted(
            zip(logistic_regression_model.coef_[0], X_train.columns),
            reverse=True)[:10]:
        print(name, importance)

    results(logistic_regression_prediction, lrm_prediction_proba)
    plot_matrix(cm, "Logistic regression")
    plot_auc(lrm_prediction_proba, "logistic regression")


def plot_matrix(cm, name):
    display_labels = ["Benign", "Pathogenic"]
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
    n_class = 2

    for i in range(n_class):
        fpr[i], tpr[i], thresh[i] = roc_curve(y_test, prediction_proba[:, i],
                                              pos_label=i)

    plt.plot(fpr[0], tpr[0], linestyle='--', color='orange', label='Benign')
    #plt.plot(fpr[1], tpr[1], linestyle='--', color='green', label='Drug response')
    #plt.plot(fpr[2], tpr[2], linestyle='--', color='red', label='Likely pathogenic')
    plt.plot(fpr[1], tpr[1], linestyle='--', color='purple', label='Pathogenic')
    plt.plot([0, 1], [0, 1], 'k--')
    plt.title(f'Multiclass ROC curve {name}')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive rate')
    plt.legend(loc='best')
    plt.show()


def average_accuracy(iterations):
    average_acc_list = []
    average_prec_list = []
    average_recall_list = []
    average_f1_list = []
    average_roc_list = []
    x = []
    for i in range(2, iterations):
        average_acc = []
        average_prec = []
        average_recall = []
        average_f1 = []
        average_roc = []
        for r in range(0, 10):
            rfc_model = RandomForestClassifier(max_leaf_nodes=i)
            rfc_model.fit(X_train, y_train)
            rfc_prediction = rfc_model.predict(X_test)
            lrm_prediction_proba = rfc_model.predict_proba(X_test)
            average_acc.append(accuracy_score(y_test, rfc_prediction))
            average_prec.append(
                precision_score(y_test, rfc_prediction, average='weighted'))
            average_recall.append(
                recall_score(y_test, rfc_prediction, average='weighted'))
            average_f1.append(
                f1_score(y_test, rfc_prediction, average='weighted'))
            average_roc.append(
                roc_auc_score(y_test, lrm_prediction_proba, average='weighted',
                              multi_class='ovr'))
        average_acc_list.append(sum(average_acc) / len(average_acc))
        average_prec_list.append(sum(average_prec) / len(average_prec))
        average_recall_list.append(sum(average_recall) / len(average_recall))
        average_f1_list.append(sum(average_f1) / len(average_f1))
        average_roc_list.append(sum(average_roc) / len(average_roc))
        x.append(i)

    plt.plot(x, average_acc_list, label="Average accuracy")
    plt.plot(x, average_prec_list, label="Average precision")
    plt.plot(x, average_recall_list, label="Average recall")
    plt.plot(x, average_f1_list, label="Average f1")
    plt.plot(x, average_roc_list, label="Average roc", color="black")
    plt.legend()
    plt.show()

def results(prediction, prediction_proba, dataset):
    print(f"\n _____ Results _____")
    print(f"Accuracy: {accuracy_score(dataset, prediction)}")
    print(f"Precision score: {precision_score(dataset, prediction, average='weighted')}")
    print(f"Recall score: {recall_score(dataset, prediction, average='weighted')}")
    print(f"F1-score: {f1_score(dataset, prediction, average='weighted')}")
    #print(f"AUC score: {roc_auc_score(dataset, prediction_proba, average='weighted', multi_class='ovr')}")


def main():
    # lda()
    #decision_tree()
    random_forest_test()
    random_forest_train()
    #average_accuracy(50)


main()
