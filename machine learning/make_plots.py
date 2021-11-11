from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import roc_curve
from sklearn.metrics import auc
from mlxtend.plotting import plot_confusion_matrix
import matplotlib.pyplot as plt
import numpy as np

def makeplots(prediction, probability, y_test):
    # confusion matrix
    cm = confusion_matrix(y_test, prediction)
    tn, fp, fn, tp, qw, wq, fsda, sdfa, fds = confusion_matrix(y_test, prediction).ravel()

    print("FPR: " + str(fp / (fp + tn)))
    print("FNR: " + str(fn / (fn + tp)))
    print("Specificity: " + str(tn / (fp + tn)))
    print("Sensitivity: " + str(tp / (tp + fn)))
    fig, ax = plot_confusion_matrix(conf_mat=cm)
    plt.rcParams['font.size'] = 20
    plt.title("LDA")
    plt.show()

    [fpr, tpr, thr] = roc_curve(y_test, probability)
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
    print(accuracy_score(prediction, y_test))