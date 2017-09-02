import sys
import pickle
import matplotlib.pyplot as plt
from feature_format import featureFormat, targetFeatureSplit

# Read the original dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

# Remove outliers

enron_dataset = data_dict
# Read data using the defined feature list
features_list = ['poi', 'salary']
data = featureFormat(enron_dataset, features_list, sort_keys=True)

# Visualize the data to find outliers
for point in data:
    poi = point[0]
    salary = point[1]
    plt.scatter(poi, salary)

plt.xlabel('poi')
plt.ylabel('salary')
