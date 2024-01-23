import pandas as pd
import numpy as np

def topsis(data, weights, impact):
  normal_matrix = data / np.sqrt((data*data).sum())
  weighted_matrix = normal_matrix*weights
  ibest = weighted_matrix.max()
  iworst = weighted_matrix.min()

  d_best = np.sqrt((((weighted_matrix - ibest)* impact)**2).sum(axis = 1))
  d_worst = np.sqrt(((weighted_matrix - iworst)**2).sum(axis = 1))

  score = d_worst / (d_best + d_worst)
  return score

ds = pd.read_csv('/content/102103464-data.csv')

weights = [1,1,1,1,1]
impacts = [True,False,True,False,True]

topsis_col = ds.columns[1:]

ds['Topsis_Score'] = topsis(ds[topsis_col],weights, impacts)

print(f"TOPSIS score = {ds['Topsis_Score']}")

ds['Topsis_Rank'] = np.argsort(ds['Topsis_Score'])[::-1]
print(f"Topsis Rank is {ds['Topsis_Rank']+1}")

output_file = '102103464-result.csv'
ds.to_csv(output_file, index=False)
