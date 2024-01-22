import sys
import numpy as np

# Normalizing the data
def matrix_normalization(matrix):
    n_m = matrix / np.sqrt(np.sum(matrix**2, axis=0))
    return n_m

# Multiplying by weights
def weighted_normalized_matrix(n_m, weights):
    w_n_m = n_m * weights
    return w_n_m

# best and worst vals
def find_ideal_worst(w_n_m, impacts):
    best= np.empty_like(w_n_m[0])
    worst = np.empty_like(w_n_m[0])
    
    for i, impact in enumerate(impacts):
        if impact == '+':
            best[i] = np.max(w_n_m[:, i])
            worst[i] = np.min(w_n_m[:, i])
        elif impact == '-':
            best[i] = np.min(w_n_m[:, i])
            worst[i] = np.max(w_n_m[:, i])
        else:
            raise ValueError("Impacts must be either '+' or '-'")
    
    return best, worst

# Calculating the TOPSIS score
def calculate_score(w_n_m, best, worst):
    SiN = np.sqrt(np.sum((w_n_m - worst)**2, axis=1))
    SiP = np.sqrt(np.sum((w_n_m - best)**2, axis=1))
    score = SiN / (SiN + SiP)
    return score

# topsis analysis
def topsis(data, weights, impacts):
    n_m = matrix_normalization(data[1:, 1:])
    w_n_m = weighted_normalized_matrix(n_m, weights)
    best, worst = find_ideal_worst(w_n_m, impacts)
    score = calculate_score(w_n_m, best, worst)

    if data[1:, 1:].shape[0] != score.shape[0]:
        raise ValueError("Error")

    result_data = np.column_stack((data[1:, :], score))

    rank = np.argsort(result_data[:, -1])[::-1] + 1
    result_data = np.column_stack((result_data, rank))

    header = np.concatenate((data[0, :], ['TOPSIS_Score', 'Rank']))
    result_data = np.vstack((header, result_data))

    print("TOPSIS results:")
    for row in result_data:
        print(", ".join(map(str, row)))


def main():
    try:
        input_file = input("Enter the CSV filename: ")
        weights = list(map(float, input("Enter the weights separated by commas: ").split(',')))
        impacts = input("Enter the impacts separated by commas (+ or -): ").split(',')

        data = np.genfromtxt(input_file, delimiter=',', skip_header=1)

        topsis(data, weights, impacts)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()


