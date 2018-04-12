from sklearn import preprocessing
from sklearn.model_selection import train_test_split, cross_val_score, cross_val_predict, ShuffleSplit
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt
import itertools
import pandas as pd
import numpy as np
import mysqlConnection as md

model_names = []
train_accuracies = []
test_accuracies = []
cv_scores = []
class_names = ['yes', 'no']

def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        title = "Normalized confusion matrix"
    else:
        title = 'Confusion matrix, without normalization'

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

def plot_outcome_chart(predicted_values, title='Predicted outcomes'):
    objects = ('No', 'Yes')
    y_pos = np.arange(len(objects))
    values = list(predicted_values.values())
    if len(values) < 3:
        values.insert(0, 0)
    plt.bar(y_pos, values, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel('Count')
    plt.title(title)
    plt.show()
    
def plot_model_comparison(model_names, train_accuracies, test_accuracies, cv_scores):
    raw_data = pd.DataFrame(
        {'model': model_names,
         'train_accuracy': train_accuracies,
         'test_accuracy': test_accuracies,
         'cv_score': cv_scores
        })
    pos = list(range(len(raw_data['train_accuracy']))) 
    width = 0.25 
    fig, ax = plt.subplots(figsize=(20,10))
    
    plt.bar(pos, 
            raw_data['train_accuracy'], 
            width, 
            alpha=0.5, 
            color='#B3CCFF', 
            label=raw_data['model'][0]) 
    
    plt.bar([p + width for p in pos], 
            raw_data['test_accuracy'],
            width, 
            alpha=0.5, 
            color='#4D88FF', 
            label=raw_data['model'][1]) 
    
    plt.bar([p + width*2 for p in pos], 
            raw_data['cv_score'],
            width, 
            alpha=0.5, 
            color='#003399', 
            label=raw_data['model'][2])
    ax.set_ylabel('Accuracy')
    ax.set_title('Model Comparison')
    ax.set_xticks([p + 1.5 * width for p in pos])
    ax.set_xticklabels(raw_data['model'])
    plt.xlim(min(pos)-width, max(pos)+width*4)
    plt.ylim( [0, 1] )
    # Adding the legend and showing the plot
    plt.legend(['Training Accuracy', 'Testing Accuracy', 'CV Score'], loc='upper left')
    plt.grid()
    plt.show()

def build_Gaussian_model():
    class_names = ['No', 'Yes']
    
    datafull = pd.read_sql_table('model_data', md.connect())
    data = datafull[['seaport', 'landprice', 'oilreserve', 'existingplants', 'disasters', 'railroad', 'populationdensity']]
    target = datafull[['actual']]
    
    x_train, x_test, y_train, y_test = train_test_split(data, target, test_size=0.2, random_state=3)
    cv = ShuffleSplit(n_splits=5, test_size=0.2, random_state=3)
    
    GNB_clf = GaussianNB()
    
    GNB_clf.fit(x_train, y_train['actual'])
    GNB_predicted = cross_val_predict(GNB_clf, data, target['actual'])
    
    GNB_scores = cross_val_score(GNB_clf, data, target.values.ravel(), cv=cv)
    
    unique, counts = np.unique(GNB_predicted, return_counts=True)
    GNB_counts = dict(zip(unique, counts))
    
    GNB_confusion = confusion_matrix(target,GNB_predicted)
    model_names.append('GaussianNB')
    
    train_accuracy = accuracy_score(y_train, GNB_clf.predict(x_train))
    train_accuracies.append(train_accuracy)
    
    test_accuracy = accuracy_score(y_test, GNB_clf.predict(x_test))
    test_accuracies.append(test_accuracy)
    
    cv_score = accuracy_score(target, GNB_predicted)
    cv_scores.append(cv_score)
    
    print("GaussianNB Model: ")
    print("  Score of {} for training set: {:.4f}.".format(GNB_clf.__class__.__name__, train_accuracy))
    print("  Score of {} for test set: {:.4f}.".format(GNB_clf.__class__.__name__, test_accuracy))
    print("  Cross validation score: %0.2f (+/- %0.2f)" % (GNB_scores.mean(), GNB_scores.std() * 2))
    print("  Predicted values accuracy: %0.2f" % (cv_score))
    
#    plot_outcome_chart(GNB_counts)
    plt.figure()
    plot_confusion_matrix(GNB_confusion, class_names)
    plt.show()
    print(classification_report(target, GNB_predicted)) 
    print()
    
def build_AdaBoost_model():
    class_names = ['No', 'Yes']
    
    datafull = pd.read_sql_table('model_data', md.connect())
    data = datafull[['landprice', 'existingplants', 'disasters', 'railroad', 'populationdensity']]
    target = datafull[['actual']]
    
    x_train, x_test, y_train, y_test = train_test_split(data, target, test_size=0.2, random_state=3)
    cv = ShuffleSplit(n_splits=5, test_size=0.2, random_state=3)
    
    AB_clf = AdaBoostClassifier(n_estimators = 500, random_state = 3)
    AB_clf.fit(x_train, y_train['actual'])
    
    AB_predicted = cross_val_predict(AB_clf, data, target['actual'])
    AB_scores = cross_val_score(AB_clf, data, target.values.ravel(), cv=cv)
    
    unique, counts = np.unique(AB_predicted, return_counts=True)
    AB_counts = dict(zip(unique, counts))
    
    AB_confusion = confusion_matrix(target,AB_predicted)
    model_names.append('AdaBoost')
    
    train_accuracy = accuracy_score(y_train, AB_clf.predict(x_train))
    train_accuracies.append(train_accuracy)
    
    test_accuracy = accuracy_score(y_test, AB_clf.predict(x_test))
    test_accuracies.append(test_accuracy)
    
    cv_score = accuracy_score(target, AB_predicted)
    cv_scores.append(cv_score)
    
    print("AdaBoost Classifier Model: ")
    print("  Score of {} for training set: {:.4f}.".format(AB_clf.__class__.__name__, train_accuracy))
    print("  Score of {} for test set: {:.4f}.".format(AB_clf.__class__.__name__, test_accuracy))
    print("  Cross validation score: %0.2f (+/- %0.2f)" % (AB_scores.mean(), AB_scores.std() * 2))
    print("  Predicted values accuracy: %0.2f" % (accuracy_score(target, AB_predicted) ))
    
#    plot_outcome_chart(AB_counts)
    plt.figure()
    plot_confusion_matrix(AB_confusion, class_names)
    plt.show()
    print(classification_report(target, AB_predicted)) 
    print()
    
    importances = AB_clf.feature_importances_
    indices = np.argsort(importances)[::-1]
    print ('Feature Ranking: ')
    for i in range(0,4):
        print ("{} feature no.{} ({})".format(i+1,indices[i],importances[indices[i]]))

def runAllModels():
    build_Gaussian_model()
    build_AdaBoost_model()
#    plot_model_comparison(model_names, train_accuracies, test_accuracies, cv_scores)
    
#runAllModels()