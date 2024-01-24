import sys
import pandas as pd
import numpy as np

def read_input(input_file):
    data = pd.read_csv(input_file)
    X = data.iloc[:, 1:].values
    return data, X

def normalize_matrix(X):
    normalized_matrix = X / np.sqrt((X**2).sum(axis=0))
    return normalized_matrix

def calculate_weighted_matrix(normalized_matrix, weights):
    weighted_matrix = normalized_matrix * weights
    return weighted_matrix

def determine_ideal_solutions(weighted_matrix):
    ideal_positive = weighted_matrix.max(axis=0)
    ideal_negative = weighted_matrix.min(axis=0)
    return ideal_positive, ideal_negative

def calculate_separation_measures(weighted_matrix, ideal_solution):
    separation = np.sqrt(((weighted_matrix - ideal_solution)**2).sum(axis=1))
    return separation

def calculate_performance_score(separation_positive, separation_negative):
    performance_score = separation_negative / (separation_positive + separation_negative)
    return performance_score

def determine_rank(performance_score):
    rank = np.argsort(performance_score)[::-1] + 1
    return rank

def write_result(data, performance_score, rank, output_file):
    result_data = data.iloc[:, :].reset_index(drop=True)
    result_data['Score'] = performance_score
    result_data['Rank'] = rank
    result_data.to_csv(output_file, index=False)

def topsis(input_file, weights, impacts, output_file):
    data, X = read_input(input_file)
    
    normalized_matrix = normalize_matrix(X)
    
    weighted_matrix = calculate_weighted_matrix(normalized_matrix, weights)
    
    ideal_positive, ideal_negative = determine_ideal_solutions(weighted_matrix)
    
    separation_positive = calculate_separation_measures(weighted_matrix, ideal_positive)
    separation_negative = calculate_separation_measures(weighted_matrix, ideal_negative)
    
    performance_score = calculate_performance_score(separation_positive, separation_negative)
    
    rank = determine_rank(performance_score)
    
    write_result(data, performance_score, rank, output_file)

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python filename input.csv <weights> <impacts> result.csv")
        sys.exit(1)
    
    input_file = sys.argv[1]
    weights = np.array(list(map(float, sys.argv[2].split(','))))
    impacts = np.array([i for i in sys.argv[3].split(',')])
    output_file = sys.argv[4]

    if len(weights) != len(impacts):
        print("Error: Number of weights and impacts must be the same.")
        sys.exit(1)
    
    topsis(input_file, weights, impacts, output_file)
    
    print(f"TOPSIS completed successfully. Results saved to {output_file}")
