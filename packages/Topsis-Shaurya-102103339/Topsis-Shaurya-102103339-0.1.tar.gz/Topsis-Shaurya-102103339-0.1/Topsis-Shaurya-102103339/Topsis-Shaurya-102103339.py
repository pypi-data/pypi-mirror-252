import sys
import pandas as pd
import numpy as np

def check_inputs(weights, impacts, data):
    if len(weights) != len(impacts) or len(weights) != len(data.columns) - 1:
        print("Error: Number of weights, impacts, and columns must be the same.")
        sys.exit(1)

    if not all(impact in ['+', '-'] for impact in impacts):
        print("Error: Impacts must be either + or -.")
        sys.exit(1)

    if not data.iloc[:, 1:].applymap(np.isreal).all().all():
        print("Error: Non-numeric values found in data.")
        sys.exit(1)

def normalize_data(data):
    normalized_data = (data.iloc[:, 1:] - data.iloc[:, 1:].min()) / (data.iloc[:, 1:].max() - data.iloc[:, 1:].min())
    return normalized_data

def calculate_topsis_score(normalized_data, weights, impacts):
    weighted_data = normalized_data * weights

    positive_ideal = weighted_data.max()
    negative_ideal = weighted_data.min()

    distance_positive = np.sqrt(((weighted_data - positive_ideal) ** 2).sum(axis=1))
    distance_negative = np.sqrt(((weighted_data - negative_ideal) ** 2).sum(axis=1))

    topsis_score = distance_negative / (distance_negative + distance_positive)

    return topsis_score

def main():
    if len(sys.argv) != 5:
        print("Usage: python <program.py> <InputDataFile> <Weights> <Impacts> <ResultFileName>")
        sys.exit(1)

    input_file = sys.argv[1]
    weights = list(map(float, sys.argv[2].split(',')))
    impacts = sys.argv[3].split(',')
    result_file = sys.argv[4]

    try:
        data = pd.read_csv('102103339-data.csv')

        check_inputs(weights, impacts, data)

        normalized_data = normalize_data(data)

        topsis_score = calculate_topsis_score(normalized_data, weights, impacts)

        data['Topsis Score'] = topsis_score
        data['Rank'] = data['Topsis Score'].rank(ascending=False)

        data.to_csv('102103339-result.csv', index=False)

        print(f"Result saved to {result_file}")

    except FileNotFoundError:
        print("Error: File not found.")
        sys.exit(1)

if __name__ == "__main__":
    main()
