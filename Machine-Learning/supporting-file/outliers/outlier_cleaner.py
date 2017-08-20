#!/usr/bin/python
from operator import itemgetter


def outlierCleaner(predictions, ages, net_worths):
    """
        Clean away the 10% of points that have the largest
        residual errors (difference between the prediction
        and the actual net worth).

        Return a list of tuples named cleaned_data where
        each tuple is of the form (age, net_worth, error).
    """

    cleaned_data = []
    ### your code goes here
    errors = [abs(net_worth - prediction) for net_worth, prediction
              in zip(net_worths, predictions)]
    raw_data = [(age, net_worth, error) for age, net_worth, error
                in zip(ages, net_worths, errors)]
    raw_data = sorted(raw_data, key = itemgetter(2))
    total_left = int(round(len(raw_data)*0.9))
    cleaned_data = raw_data[:total_left]



    return cleaned_data
