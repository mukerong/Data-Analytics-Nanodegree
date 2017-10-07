#!/usr/bin/python

import sys
sys.path.append("../tools/")
import pickle
from collections import defaultdict
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from collections import defaultdict
from feature_format import featureFormat, targetFeatureSplit
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.feature_selection import SelectKBest
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedShuffleSplit
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import classification_report
from sklearn.pipeline import Pipeline
from tester import test_classifier

%matplotlib inline

### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".


# Select features and create variables
features_list = []

for _, value in data_dict.items():
    for k, _ in value.items():
        features_list.append(k)
    break

features_list.remove('poi')
features_list.insert(0, 'poi')
features_list.remove('email_address')

### Task 2: Remove outliers
data_dict.pop('TOTAL', 0)
data_dict.pop('THE TRAVEL AGENCY IN THE PARK',0)

### Task 3: Create new feature(s) and append to features list
### Store to enron_dataset for easy export below.

# bonus/salary ratio
for employee, features in data_dict.items():
    if features['salary'] != "NaN" and features['bonus'] != 'NaN':
        features['bonus_salary_ratio'] = \
        float(features['salary'])/float(features['bonus'])
    else:
        features['bonus_salary_ratio'] = "NaN"
features_list.append('bonus_salary_ratio')

# from_this_person_to_poi/from_messages ratio
for employee, features in data_dict.items():
    if features['from_this_person_to_poi'] != "NaN" and features['from_messages'] != 'NaN':
        features['from_this_person_to_poi_percentage'] = \
        float(features['from_this_person_to_poi'])/float(features['from_messages'])
    else:
        features['from_this_person_to_poi_percentage'] = "NaN"
features_list.append('from_this_person_to_poi_percentage')

# from_poi_to_this_person/to_messages ratio
for employee, features in data_dict.items():
    if features['from_poi_to_this_person'] != "NaN" and features['to_messages'] != 'NaN':
        features['from_poi_to_this_person_percentage'] = \
        float(features['from_poi_to_this_person'])/float(features['to_messages'])
    else:
        features['from_poi_to_this_person_percentage'] = "NaN"
features_list.append('from_poi_to_this_person_percentage')


# Since there are a lot of missing values hidden in the dataset, I will
# use the mean toe replace NaN.
email_features = ['to_messages',
                  'from_poi_to_this_person',
                  'from_poi_to_this_person_percentage',
                  'from_messages',
                  'from_this_person_to_poi',
                  'from_this_person_to_poi_percentage',
                  'shared_receipt_with_poi']


email_feature_sums = defaultdict(lambda:0)
email_feature_counts = defaultdict(lambda:0)

for employee, features in data_dict.iteritems():
    for feature in email_features:
        if features[feature] != "NaN":
            email_feature_sums[feature] += features[feature]
            email_feature_counts[feature] += 1

email_feature_means = {}
for feature in email_features:
    email_feature_means[feature] = float(email_feature_sums[feature]) / float(email_feature_counts[feature])

for employee, features in data_dict.iteritems():
    for feature in email_features:
        if features[feature] == "NaN":
            features[feature] = email_feature_means[feature]


enron_dataset = data_dict


### Extract features and labels from dataset for local testing
data = featureFormat(enron_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)

features_train, features_test, labels_train, labels_test = \
    train_test_split(features, labels, test_size=0.2, random_state=42)

scaler = MinMaxScaler()
features_train_std = scaler.fit_transform(features_train)
features_test_std = scaler.transform(features_test)

select = SelectKBest()

cv = StratifiedShuffleSplit(
    n_splits = 100,
    test_size = 0.3,
    random_state = 6
    )

### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html

# Provided to give you a starting point. Try a variety of classifiers.

'''
I will try several different classifiers here. Detials will all under task 5.
'''


### Task 5: Tune your classifier to achieve better than .3 precision and recall
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info:
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

# Example starting point. Try investigating other evaluation techniques!

'''
# Gassian Naive Bayes (No Tuning)

clf = GaussianNB()
clf.fit(features_train_std, labels_train)
pred = clf.predict(features_test_std)

test_classifier(clf, enron_dataset, features_list)
'''


# Decision Tree

steps = [
    ('feature_selection', select),
    ('tree', DecisionTreeClassifier())
]

pipeline = Pipeline(steps)

parameters = {
    'feature_selection__k': [5, 6, 7, 8, 'all'],
    'tree__min_samples_split': [2, 3, 5],
    'tree__min_samples_leaf': [1, 2, 3]
}

grid = GridSearchCV(pipeline, param_grid=parameters, cv=cv, scoring='f1', error_score=0)
grid.fit(features_train_std, labels_train)
clf=grid.best_estimator_
print "\n", "Best parameters are: ", grid.best_params_, "\n"

features_selected = [features_list[i]
                     for i in clf.named_steps['feature_selection'].get_support(indices=True)]
features_selected.insert(0, 'poi')

print test_classifier(clf, enron_dataset, features_selected)

features_list = features_selected



'''
# Random Forest
steps = [
    ('feature_selection', select),
    ('rf', RandomForestClassifier())
]

pipeline = Pipeline(steps)

parameters = {
    'feature_selection__k': [5, 6, 7, 8, 'all'],
    'rf__n_estimators': [10, 20, 30, 40],
    'rf__min_samples_split': [2, 5, 10],
    'rf__criterion': ['gini', 'entropy'],
    'rf__random_state': [10]
}

grid = GridSearchCV(pipeline, param_grid=parameters, scoring='f1',
    cv=cv, error_score=0)

grid.fit(features_train_std, labels_train)

clf = grid.best_estimator_
print "\n", "Best parameters are: ", grid.best_params_, "\n"

features_selected = [features_list[i]
                     for i in clf.named_steps['feature_selection'].get_support(indices=True)]
features_selected.insert(0, 'poi')

print test_classifier(clf, enron_dataset, features_selected)

features_list = features_selected
'''

'''
# SVM
estimators =[
             ('feature_selection', SelectKBest()),
             ('svm', SVC())
]

pipeline = Pipeline(estimators)

parameters = {
    'feature_selection__k': [4, 5, 6, 7, 'all'],
    'svm__kernel': ['linear', 'rbf'],
    'svm__C': [0.001, 0.01, 0.1, 1, 3],
    'svm__gamma': [0.001, 0.01, 0.1]
}

grid = GridSearchCV(pipeline, param_grid=parameters, scoring='f1',
    cv=cv, error_score=0)

grid.fit(features_train_std, labels_train)

clf = grid.best_estimator_
print "\n", "Best parameters are: ", grid.best_params_, "\n"

features_selected = [features_list[i]
                     for i in clf.named_steps['feature_selection'].get_support(indices=True)]
features_selected.insert(0, 'poi')

print test_classifier(clf, enron_dataset, features_selected)

features_list = features_selected
'''

'''
# KNN
estimators = [
    ('feature_selection', select),
    ('knn', KNeighborsClassifier())
]

pipeline = Pipeline(estimators)

parameters = {
    'feature_selection__k': [4, 5, 6, 7, 'all'],
    'knn__n_neighbors': [2, 3, 4, 5],
    'knn__leaf_size': [1, 10, 20, 30],
    'knn__algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute']
}

grid = GridSearchCV(pipeline, param_grid=parameters, scoring='f1', cv=cv, error_score=0)
grid.fit(features_train_std, labels_train)

clf = grid.best_estimator_
print "\n", "Best parameters are: ", grid.best_params_, "\n"

features_selected = [features_list[i]
                     for i in clf.named_steps['feature_selection'].get_support(indices=True)]
features_selected.insert(0, 'poi')

print test_classifier(clf, enron_dataset, features_selected)

features_list = features_selected
'''

'''
# AdaBoost
estimators = [
    ('feature_selection', select),
    ('adb', AdaBoostClassifier())
]

pipeline = Pipeline(estimators)

parameters = {
    'feature_selection__k': [3, 4, 5, 6, 7, 'all'],
    'adb__n_estimators': [10, 50, 100],
    'adb__learning_rate': [0.001, 0.01, 0.1, 1, 2],
    'adb__algorithm': ['SAMME', 'SAMME.R']
}

grid = GridSearchCV(pipeline, param_grid=parameters, scoring='f1', cv=cv, error_score=0)
grid.fit(features_train_std, labels_train)

clf = grid.best_estimator_
print "\n", "Best parameters are: ", grid.best_params_, "\n"

features_selected = [features_list[i]
                     for i in clf.named_steps['feature_selection'].get_support(indices=True)]
features_selected.insert(0, 'poi')

print test_classifier(clf, enron_dataset, features_selected)

features_list = features_selected
'''

### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

dump_classifier_and_data(clf, enron_dataset, features_list)
