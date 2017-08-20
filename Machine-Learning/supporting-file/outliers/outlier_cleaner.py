#!/usr/bin/python


def outlierCleaner(predictions, ages, net_worths):
    """
        Clean away the 10% of points that have the largest
        residual errors (difference between the prediction
        and the actual net worth).

        Return a list of tuples named cleaned_data where
        each tuple is of the form (age, net_worth, error).
    """

    cleaned_data = []
    print net_worths
    ### your code goes here
    errors = [abs(net_worth - prediction) for net_worth, prediction
              in zip(net_worths, predictions)]
    raw_data = [(age, net_worth, error) for age, net_worth, error
                in zip(ages, net_worths, errors)]
    print raw_data


    return cleaned_data


outlierCleaner([1, 2, 3], [1, 2, 3], [3, 2, 6])
