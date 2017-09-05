from features import enron_dataset, features_list
import sys
sys.path.append("../tools/")
from feature_format import featureFormat, targetFeatureSplit
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


data = featureFormat(enron_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)

# selector = SelectPercentile(features, percentile=10)
# selector.fit()

features_train, features_test, labels_train, labels_test = train_test_split(
    features, labels, test_size=0.2, random_state=1
)

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
for train_indices, test_indices in kfold.split(labels):
    features_train = [features[i] for i in train_indices]
    features_test = [features[i] for i in test_indices]
    labels_train = [labels[i] for i in train_indices]
    labels_test = [labels[i] for i in test_indices]

    clf = GridSearchCV(pipeline, param_grid=parameters,
                       scoring='f1',error_score=0)

    clf.fit(features_train, labels_train)
    adaboost_prediction = clf.predict(features_test)

    print "adaboost accuracy score: ", \
        accuracy_score(labels_test, adaboost_prediction)
    print "adaboost precision_score: ", \
        precision_score(labels_test, adaboost_prediction)
    print "adaboost recall_score", \
        recall_score(labels_test, adaboost_prediction)
