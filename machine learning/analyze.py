# Import dependencies
import numpy as np
import seaborn as sns
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, \
    precision_score, accuracy_score, \
    recall_score, roc_auc_score, roc_curve, f1_score
from mlxtend.plotting import plot_confusion_matrix
from matplotlib import pyplot as plt
from sklearn.tree import DecisionTreeClassifier
import pickle

# initiate seaborn plugin
sns.set()

# Read the Machine learning training file
df = pd.read_csv('ML data.tsv', sep='\t')

# Select all columns except genes
X = df.iloc[:, np.r_[5, 6, 7, 25, 27:31, 33:77]]

# Select class column
y = df['CLNSIG NUM']

# Split the train and test set with 80% trainingset and 20% testset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20,
                                                    random_state=27)


def lda():
    """Train and analyze Linear Discriminant Model
    """    
    print("##### Linear discriminant analysis #####")

    # Train model using the trainingset
    lda = LinearDiscriminantAnalysis()
    lda.fit(X_train, y_train)

    # Use model to predict testset
    lda_prediction = lda.predict(X_test)
    lda_prediction_proba = lda.predict_proba(X_test)
    cm = confusion_matrix(y_test, lda_prediction)

    for importance, name in sorted(zip(lda.coef_[0], X_train.columns),
                                   reverse=True):
        print(name, importance)

    results(lda_prediction, lda_prediction_proba, y_test)
    plot_matrix(cm, "Linear discriminant analysis")
    plot_auc(lda_prediction_proba, "linear discriminant analysis", y_test)


def decision_tree():
    """Train and fit a decision tree and generate a CM
    """
    print("##### Decision tree #####")

    # Train model using the trainingset
    clf = DecisionTreeClassifier(max_depth=10)
    clf_model = clf.fit(X_train, y_train)

     # Use model to predict testset
    clf_prediction = clf_model.predict(X_test)
    clf_prediction_proba = clf.predict_proba(X_test)
    cm = confusion_matrix(y_test, clf_prediction)
    for importance, name in sorted(
            zip(clf.feature_importances_, X_train.columns),
            reverse=True):
        print(name, importance)

    results(clf_prediction, clf_prediction_proba, y_test)
    plot_matrix(cm, "Decision tree")
    plot_auc(clf_prediction_proba, "decision tree", y_test)


def random_forest_train():
    """Train and analyze Random Forest Model and cross-validate on training set
    """    
    print("##### Random forest #####")

    # Train model using the trainingset
    rfc = RandomForestClassifier(max_depth=10)
    rfc_model = rfc.fit(X_train, y_train)

    # Use model to predict testset
    rfc_prediction = rfc_model.predict(X_train)
    rfc_prediction_proba = rfc.predict_proba(X_train)
    cm = confusion_matrix(y_train, rfc_prediction)

    for importance, name in sorted(
        zip(
            rfc.feature_importances_, X_train.columns), reverse=True)[:10]:
        print(name, importance)

    results(rfc_prediction,  rfc_prediction_proba, y_train)
    plot_matrix(cm, "Random forest")
    plot_auc(rfc_prediction_proba, "random forest", y_train)



def random_forest_test():
    """Train and analyze Random Forest Model and test with testset
    """
    print("##### Random forest #####")

    # Train model using the trainingset
    rfc = RandomForestClassifier(max_depth=10)
    rfc_model = rfc.fit(X_train, y_train)

    # Use model to predict testset
    rfc_prediction = rfc_model.predict(X_test)
    rfc_prediction_proba = rfc.predict_proba(X_test)
    cm = confusion_matrix(y_test, rfc_prediction)

    for importance, name in sorted(
            zip(rfc.feature_importances_, X_train.columns),
            reverse=True)[:10]:
        print(name, importance)

    results(rfc_prediction, rfc_prediction_proba, y_test)
    plot_matrix(cm, "Random forest test validation")
    plot_auc(rfc_prediction_proba, "Random forest test validation", y_test)



def logistic():
    """Train and analyze Logistic Regression Model and test with testset
    """
    print("##### Logistic regression #####")

    # Train model using the trainingset
    logistic_regression_model = LogisticRegression()
    logistic_regression_model.fit(X_train, y_train)

    # Use model to predict testset
    logistic_regression_prediction = logistic_regression_model.predict(X_test)
    lrm_prediction_proba = logistic_regression_model.predict_proba(X_test)
    cm = confusion_matrix(y_test, logistic_regression_prediction)

    for importance, name in sorted(
            zip(logistic_regression_model.coef_[0], X_train.columns),
            reverse=True)[:10]:
        print(name, importance)

    results(logistic_regression_prediction, lrm_prediction_proba, y_test)
    plot_matrix(cm, "Logistic regression")
    plot_auc(lrm_prediction_proba, "logistic regression", y_test)


def plot_matrix(cm, name):
    """Plot confusion matrix

    Args:
        cm: The confusion matrix array
        name: String with name
    """
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


def plot_auc(prediction_proba, name, dataset):
    """Generate a ROC curve plot using probabilities and test variables

    Args:
        prediction_proba: Array with probabilites per prediction
        name: Name of the plot title
    """
    fpr = {}
    tpr = {}
    thresh = {}
    n_class = 2

    # Get fpr and tpr and create roc curve
    for i in range(n_class):
        fpr[i], tpr[i], thresh[i] = roc_curve(dataset, prediction_proba[:, i],
                                              pos_label=i)
    # Plot ROC curve
    plt.plot(fpr[0], tpr[0], linestyle='--', color='orange', label='Benign')
    plt.plot(fpr[1], tpr[1], linestyle='--',
             color='purple', label='Pathogenic')
    plt.plot([0, 1], [0, 1], 'k--')
    plt.title(f'ROC curve {name}')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive rate')
    plt.legend(loc='best')
    plt.show()


def average_accuracy(iterations):
    """Calculate the average accuracy, precision, recall, F1 and AUC
    for each iteration.

    Args:
        iterations : The amount of iterations the parameter is tested for.
    """
    # Make lists
    average_acc_list = []
    average_acc_list_train = []
    average_prec_list = []
    average_recall_list = []
    average_f1_list = []
    average_roc_list = []
    x = []
    # Loop over the amount of iterations given as parameter
    for i in range(1, iterations):
        # Make a list for each run
        average_acc = []
        average_acc_train = []
        average_prec = []
        average_recall = []
        average_f1 = []
        average_roc = []
        # To average scores the model is made 10 times for every iteration
        for r in range(0, 10):
            # Test the max depth for this classifier
            rfc_model = RandomForestClassifier(max_depth=i)
            rfc_model.fit(X_train, y_train)
            rfc_prediction = rfc_model.predict(X_test)
            # Calculate prediction & probability
            rfc_prediction_train = rfc_model.predict(X_train)
            rfc_prediction_proba = rfc_model.predict_proba(X_test)
            # add the scores to a list
            average_acc.append(accuracy_score(y_test, rfc_prediction))
            average_acc_train.append(
                accuracy_score(y_train, rfc_prediction_train))
            average_prec.append(precision_score(y_test, rfc_prediction))
            average_recall.append(recall_score(y_test, rfc_prediction))
            average_f1.append(f1_score(
                y_test, rfc_prediction)
            )
            average_roc.append(roc_auc_score(y_test, rfc_prediction_proba[:, 1]))
        # Average the scores and add them as a data point to the list
        average_acc_list.append(sum(average_acc) / len(average_acc))
        average_acc_list_train.append(
            sum(average_acc_train) / len(average_acc_train))
        average_prec_list.append(sum(average_prec) / len(average_prec))
        average_recall_list.append(sum(average_recall) / len(average_recall))
        average_f1_list.append(sum(average_f1) / len(average_f1))
        average_roc_list.append(sum(average_roc) / len(average_roc))
        x.append(i)
    # Plot the averaged values in a figure
    print(x)
    print(average_acc_list)
    plt.plot(x, average_acc_list, label="Average accuracy test")
    plt.plot(x, average_acc_list_train, label="Average accuracy train")
    plt.plot(x, average_prec_list, label="Average precision")
    plt.plot(x, average_recall_list, label="Average recall")
    plt.plot(x, average_f1_list, label="Average f1")
    plt.plot(x, average_roc_list, label="Average roc", color="black")
    plt.title(f'ML model metrics accuracy vs iterations')
    plt.xlabel('Iteration')
    plt.ylabel('Average value')
    plt.legend()
    plt.show()


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



def main():
    # Call functions to analyze performance
    lda()
    logistic()
    decision_tree()
    random_forest_test()
    random_forest_train()
    average_accuracy(10)


main()
