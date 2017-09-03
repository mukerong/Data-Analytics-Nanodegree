import sys
sys.path.append("../tools/")
import pickle
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix
from feature_format import featureFormat, targetFeatureSplit

# Read the original dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

# Remove outliers and create a new data dictionary
enron_dataset = data_dict

# Read data using the defined feature list
features_list = ['poi', 'salary']
data = featureFormat(enron_dataset, features_list, sort_keys=True)

# Visualize the data to find outliers
enron_dataframe = pd.DataFrame(enron_dataset.values())
employees = pd.Series(enron_dataset.keys())
enron_dataframe.set_index(employees, inplace=True)
