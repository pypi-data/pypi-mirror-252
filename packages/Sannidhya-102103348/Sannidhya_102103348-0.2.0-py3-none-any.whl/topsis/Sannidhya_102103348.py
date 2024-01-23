import pandas as pd
import numpy as np
import sys
#from sklearn.preprocessing import normalize

def topsis(df, weights, impacts):
    """
    TOPSIS algorithm implementation.

    Parameters:
    - df: DataFrame containing numeric values.
    - weights: List of weights for each column. Default is None (equal weights).
    - impacts: List of impact values for each column (+1 or -1). Default is None (maximize all columns).

    Returns:
    - DataFrame with TOPSIS score and rank.
    """
    # Check if weights are provided, else assign equal weights
    if weights is None:
        weights = [1] * (df.shape[1] - 1)

    # Check if impacts are provided, else assign +1 (maximize)
    if impacts is None:
        impacts = [1] * (df.shape[1] - 1)

    # Normalize the data
    normalized_df = df.copy()
    for i, col in enumerate(df.columns[1:]):
        normalized_df[col] = df[col] / np.linalg.norm(df[col])
    # Multiply each column by its weight
    weighted_df = normalized_df * weights

    # Calculate ideal and negative-ideal solutions
    ideal_best = np.max(weighted_df, axis=0)
    ideal_worst = np.min(weighted_df, axis=0)

    # Calculate the separation measures
    separation_best = np.linalg.norm(weighted_df - ideal_best, axis=1)
    separation_worst = np.linalg.norm(weighted_df - ideal_worst, axis=1)

    # Calculate the TOPSIS score
    topsis_score = separation_worst / (separation_best + separation_worst)

    # Add TOPSIS score and rank to the original DataFrame
    df['TOPSIS Score'] = topsis_score
    df['Rank'] = df['TOPSIS Score'].rank(ascending=False)

    return df

# Read the CSV file
if len(sys.argv) != 5:
    print(sys.argv)
    print("Usage: python topsis.py inputFileName weights_and_impacts resultFileName")
else:
    file_path = input()  # Replace with your file path
    w=input()
    i=input()
    weights=np.array([int(x) for x in w.split(',')])
    impacts=np.array([1 if x=='+' else -1 for x in i.split(',')])
    df = pd.read_csv(file_path, index_col=0)

file_path = sys.argv[1]  # Replace with your file path
w=sys.argv[2]
i=sys.argv[3]
weights=np.array([int(x) for x in w.split(',')])
impacts=np.array([1 if x=='+' else -1 for x in i.split(',')])
df = pd.read_csv(file_path, index_col=0)

# Apply TOPSIS algorithm
result_df = topsis(df,weights,impacts)

# Display the result
print(result_df)
result_df.to_csv('102103348-result.csv')