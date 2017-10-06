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


# Read the data to a dataframe
enron_dataframe = pd.DataFrame(data_dict.values())
employees = pd.Series(data_dict.keys())
enron_dataframe.set_index(employees, inplace=True)

enron_dataframe = enron_dataframe.apply(lambda x:
                                        pd.to_numeric(x, errors='coerce'))

poi = pd.Series([0, 1], index=[False, True])
enron_dataframe['poi'] = enron_dataframe.poi.map(poi)

# Draw the scatter plot with salary and poi to see if there are any outliers
enron_dataframe.plot.scatter(x='poi', y='salary')

# Remove Outliers
data_dict.pop('TOTAL', 0)

# Visualize the rest of the data to find outliers
for col in enron_dataframe.columns:
    enron_dataframe.plot.scatter(x='poi', y=col)
