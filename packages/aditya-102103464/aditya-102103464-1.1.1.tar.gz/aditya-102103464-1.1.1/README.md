# TOPSIS Python Package

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

TOPSIS (Technique for Order Preference by Similarity to Ideal Solution) is a method for multicriteria decision analysis. This Python package provides a simple implementation of TOPSIS for ranking alternatives based on multiple criteria.

## Installation

You can install the `topsis` package using pip:

pip install topsis-Aditya-102103464

# Usage

import numpy as np
from topsis-Aditya-102103464 import topsis

# Example decision matrix
import .csv data file
# Criteria weights
weights = [1, 1, 1, 1]

# Impact criteria
impacts = [True, True, True, True]

# Perform TOPSIS analysis
scores = topsis(matrix, weights, is_benefit)
ranking = np.argsort(scores)[::-1]
print("Scores:", scores)
print("Ranking:", ranking+1)

# Output 

A .csv file containing input columns with two additional columns ie. topsis score and ranking will be generated.