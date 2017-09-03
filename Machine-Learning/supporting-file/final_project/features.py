from outliers import data_dict
import sys
sys.path.append("../tools/")

# Create new features
# bonus/salary ratio
for employee, features in data_dict:
    if features['salary'] != "NaN" and features['bonus'] != 'NaN':
        features['bonus_salary_ratio'] = float(features['salary'])/float(features['bonus'])
    else:
        features['bonus_salary_ratio'] = "NaN"


# Select features and create variables
features_list = ['poi','salary', 'bonus', 'exercised_stock_options']


# Feature transformation

# selector = SelectPercentile(features, percentile=10)
# selector.fit()
