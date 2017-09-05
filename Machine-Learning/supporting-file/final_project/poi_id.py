#!/usr/bin/python

import sys
import pickle
sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_selection import SelectKBest, SelectPercentile
from sklearn.model_selection import train_test_split, KFold, GridSearchCV
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn import tree
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.decomposition import PCA

### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".

for employee, features in data_dict.items():
    if features['salary'] != "NaN" and features['bonus'] != 'NaN':
        features['bonus_salary_ratio'] = \
        float(features['salary'])/float(features['bonus'])
    else:
        features['bonus_salary_ratio'] = "NaN"

# from_this_person_to_poi/from_messages ratio
for employee, features in data_dict.items():
    if features['from_this_person_to_poi'] != "NaN" and features['from_messages'] != 'NaN':
        features['from_this_person_to_poi_percentage'] = \
        float(features['from_this_person_to_poi'])/float(features['from_messages'])
    else:
        features['from_this_person_to_poi_percentage'] = "NaN"

# from_poi_to_this_person/to_messages ratio
for employee, features in data_dict.items():
    if features['from_poi_to_this_person'] != "NaN" and features['to_messages'] != 'NaN':
        features['from_poi_to_this_person_percentage'] = \
        float(features['from_poi_to_this_person'])/float(features['to_messages'])
    else:
        features['from_poi_to_this_person_percentage'] = "NaN"

# Select features and create variables
features_list = ['poi','salary', 'bonus', 'exercised_stock_options',
                 'bonus_salary_ratio', 'from_this_person_to_poi',
                 'from_poi_to_this_person']

### Task 2: Remove outliers
data_dict.pop('TOTAL', 0)

### Task 3: Create new feature(s)
### Store to enron_dataset for easy export below.
enron_dataset = data_dict

### Extract features and labels from dataset for local testing
data = featureFormat(enron_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)

### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html

# Provided to give you a starting point. Try a variety of classifiers.

### Task 5: Tune your classifier to achieve better than .3 precision and recall
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info:
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

# Example starting point. Try investigating other evaluation techniques!
from sklearn.model_selection import train_test_split
features_train, features_test, labels_train, labels_test = \
    train_test_split(features, labels, test_size=0.3, random_state=42)


'''
# Decision Tree
scaler = MinMaxScaler()
scaler.fit(features_train)
scaled_features_train = scaler.transform(features_train)
scaled_features_test = scaler.transform(features_test)

parameters = {'min_samples_split': (2, 5, 10)}
tree = GridSearchCV(tree.DecisionTreeClassifier(), parameters)
tree.fit(scaled_features_train, labels_train)
tree_prediction = tree.predict(scaled_features_test)
print "decision tree accuracy score: ", \
    accuracy_score(labels_test, tree_prediction)
print "decision tree precision_score: ", \
    precision_score(labels_test, tree_prediction)
print "decision treere call_score", \
    recall_score(labels_test, tree_prediction)
'''

'''
# Use pipeline to tune SVM
estimators =[('scaler', MinMaxScaler()),
             ('feature_selection', SelectKBest()),
             ('svm', SVC())
             ]
pipeline = Pipeline(estimators)

parameters = {
    'feature_selection__k': [2, 3, 4, 5, 6, 'all'],
    'svm__kernel': ['linear', 'rbf'],
    'svm__C': [0.1, 1, 10, 100, 1000, 10000],
    'svm__gamma': [0.1, 0.01, 0.001, 0.0001]
}

clf = GridSearchCV(pipeline, param_grid=parameters, scoring='f1',error_score=0)
clf.fit(features_train, labels_train)
svc_prediction = clf.predict(features_test)

print "svc accuracy score: ", \
    accuracy_score(labels_test, svc_prediction)
print "svc precision_score: ", \
    precision_score(labels_test, svc_prediction)
print "svc recall_score", \
    recall_score(labels_test, svc_prediction)
'''

'''
# Use pipeline to tune KNN
estimators = [
    ('scaler', MinMaxScaler()),
    ('feature_selection', SelectKBest()),
    ('knn', KNeighborsClassifier())
]
pipeline = Pipeline(estimators)

parameters = {
    'feature_selection__k': [2, 3, 4, 5, 6, 'all'],
    'knn__n_neighbors': [1, 2, 3, 4, 5],
    'knn__leaf_size': [1, 10, 30, 60],
    'knn__algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute']
}

clf = GridSearchCV(pipeline, param_grid=parameters, scoring='f1',error_score=0)
clf.fit(features_train, labels_train)
knn_prediction = clf.predict(features_test)

print "knn accuracy score: ", \
    accuracy_score(labels_test, knn_prediction)
print "knn precision_score: ", \
    precision_score(labels_test, knn_prediction)
print "knn recall_score", \
    recall_score(labels_test, knn_prediction)
'''

# Use KFold and AdaBoost
estimators = [
    ('scaler', MinMaxScaler()),
    ('feature_selection', SelectKBest()),
    ('adaboost', AdaBoostClassifier())
]
pipeline = Pipeline(estimators)

parameters = {
    'feature_selection__k': [2, 3, 4, 5, 6, 'all'],
    'adaboost__n_estimators': [10, 50, 100],
    'adaboost__learning_rate': [1, 5, 10],
    'adaboost__algorithm': ['SAMME', 'SAMME.R']
}

kfold = KFold(n_splits=3, shuffle=True)

gs = GridSearchCV(pipeline, param_grid=parameters,
                   scoring='f1',error_score=0, cv=kfold)

gs.fit(features, labels)
clf = gs.best_estimator_
adaboost_prediction = clf.predict(features_test)

print "adaboost accuracy score: ", \
    accuracy_score(labels_test, adaboost_prediction)
print "adaboost precision_score: ", \
    precision_score(labels_test, adaboost_prediction)
print "adaboost recall_score", \
    recall_score(labels_test, adaboost_prediction)


### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

dump_classifier_and_data(clf, enron_dataset, features_list)
