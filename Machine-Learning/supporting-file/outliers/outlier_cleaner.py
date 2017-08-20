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

    ### your code goes here
    errors = [abs(net_worths - predictions) for net_worths, predictions
              in zip(net_worths, predictions)]
    errors = sorted(errors)
    print errors

    return cleaned_data


outlierCleaner([1, 2, 3], [1, 2, 3], [3, 2, 6])
