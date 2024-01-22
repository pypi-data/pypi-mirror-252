#TOPSIS (Technique for Order of Preference by Similarity to Ideal Solution) is a Python package for performing TOPSIS analysis on a given dataset.

## Installation

You can install the package using pip:


pip install topsis-aayushi-102103421


## USAGE
import pandas as pd
from topsis_package import topsis

## Sample data
data = pd.DataFrame({
    'P1': [3, 4, 5, 2],
    'P2': [5, 2, 3, 4],
    'P3': [2, 3, 4, 5],
    'P4': [4, 5, 2, 3],
    'P5': [1, 2, 3, 4],
})

## Sample weights and impacts
weights = [1, 1, 1, 1, 1]
impacts = [1, -1, 1, 1, -1]

## Perform TOPSIS analysis
topsis_scores = topsis(data, weights, impacts)

## Display TOPSIS scores
print("TOPSIS Scores:")
print(topsis_scores)
