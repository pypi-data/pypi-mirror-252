# topsis_package/topsis_package/topsis.py

import pandas as pd
import numpy as np

def topsis(data, weights, impacts):
    """
    Perform TOPSIS analysis on a given dataset.

    Parameters:
    - data (pd.DataFrame): The decision matrix.
    - weights (list): Weights for each criterion.
    - impacts (list): Impacts for each criterion (1 for maximization, -1 for minimization).

    Returns:
    - pd.Series: TOPSIS scores for each row in the decision matrix.
    """
    # Normalize the decision matrix
    normalized_matrix = data / np.sqrt((data**2).sum())

    # Multiply normalized matrix by weights
    weighted_matrix = normalized_matrix * weights

    # Determine the ideal and negative-ideal solutions
    ideal_best = weighted_matrix.max()
    ideal_worst = weighted_matrix.min()

    # Calculate the Euclidean distances to the ideal best and worst solutions
    dist_best = np.sqrt(((weighted_matrix - ideal_best)**2).sum(axis=1))
    dist_worst = np.sqrt(((weighted_matrix - ideal_worst)**2).sum(axis=1))

    # Calculate the TOPSIS score
    topsis_score = dist_worst / (dist_best + dist_worst)

    return topsis_score
