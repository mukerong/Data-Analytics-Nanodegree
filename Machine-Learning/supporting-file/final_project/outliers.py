import sys
sys.path.append("../tools/")
import pickle
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from feature_format import featureFormat, targetFeatureSplit

# Read the original dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

# Remove outliers and create a new data dictionary
data_dict.pop('TOTAL', 0)
enron_dataset = data_dict

# Read data using the defined feature list
features_list = ['poi', 'salary']
data = featureFormat(enron_dataset, features_list, sort_keys=True)

# Read the data to a dataframe
enron_dataframe = pd.DataFrame(enron_dataset.values())
employees = pd.Series(enron_dataset.keys())
enron_dataframe.set_index(employees, inplace=True)

enron_dataframe = enron_dataframe.apply(lambda x:
                                        pd.to_numeric(x, errors='coerce'))

poi = pd.Series([0, 1], index=[False, True])
enron_dataframe['poi'] = enron_dataframe.poi.map(poi)

# Visualize the data to find outliers
enron_dataframe.plot.scatter(x='poi', y='salary')
