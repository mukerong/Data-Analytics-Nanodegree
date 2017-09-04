from features import enron_dataset, features_list
import sys
sys.path.append("../tools/")
from feature_format import featureFormat, targetFeatureSplit
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_selection import SelectKBest, SelectPercentile
from sklearn.model_selection import train_test_split, KFold, GridSearchCV
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn import tree
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


# Use pipeline to run multi-stage operations
scaler = MinMaxScaler()
scaler.fit(features_train)
scaled_features_train = scaler.transform(features_train)
scaled_features_test = scaler.transform(features_test)

'''
# Decision Tree
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

# SVM
parameters = {'kernel': ('linear', 'rbf'), 'C': (1, 10)}
svc = SVC()
svc = GridSearchCV(svc, parameters)
svc.fit(scaled_features_train, labels_train)
svc_prediction = svc.predict(scaled_features_test)

print "svc accuracy score: ", \
    accuracy_score(labels_test, svc_prediction)
print "svc precision_score: ", \
    precision_score(labels_test, svc_prediction)
print "svc recall_score", \
    recall_score(labels_test, svc_prediction)
