from outliers import data_dict
import sys
sys.path.append("../tools/")

# Create new features
# bonus/salary ratio
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

enron_dataset = data_dict
