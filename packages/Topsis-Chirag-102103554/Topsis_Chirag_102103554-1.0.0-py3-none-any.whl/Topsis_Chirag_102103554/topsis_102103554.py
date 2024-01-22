import pandas as pd
import numpy as np
import sys
import math


def is_numeric(column):
    try:
        column.astype(float)
        return True
    except ValueError:
        return False


def topsis(input_file, weights, impacts, output_file):
    try:
        # Read the input CSV file
        df = pd.read_csv(input_file)

        if len(sys.argv) != 5:
            raise ValueError('Incorrect number of parameters. Please provide inputFileName, Weights, Impacts, and resultFileName.')

        if not df.empty:
            if len(df.columns) < 3:
                raise ValueError('Input file must contain three or more columns!')

            if len(weights) != (len(df.columns) - 1) or len(impacts) != (len(df.columns) - 1):
                raise ValueError('Number of weights, impacts, and columns are not the same!')

            impacts = [1 if i == '+' else 0 for i in impacts]

            if not all(i in [0, 1] for i in impacts):
                raise ValueError('Impacts must be either +ve or -ve.')

            if not all(isinstance(w, (int, float)) for w in weights):
                raise ValueError('Weights must be numeric values.')

            if not all(is_numeric(df.iloc[:, i]) for i in range(1, len(df.columns))):
                raise ValueError('Columns from 2nd to last must contain numeric values.')
            
            rows = df.shape[0]

            # Normalize the matrix
            for col in range(1, len(df.columns)):
                rss = np.linalg.norm(df.iloc[:, col])
                df.iloc[:, col] = df.iloc[:, col] / rss

            # Multiply by weights
            for col in range(1, len(df.columns)):
                df.iloc[:, col] = df.iloc[:, col] * weights[col - 1]

            # Calculate V+ and V-
            v_best = df.max(axis=0)[1:]
            v_worst = df.min(axis=0)[1:]

            # Calculate Si+ and Si-
            s_best = [math.sqrt(sum((df.iloc[row, 1:] - v_best) ** 2)) for row in range(rows)]
            s_worst = [math.sqrt(sum((df.iloc[row, 1:] - v_worst) ** 2)) for row in range(rows)]

            pi = np.array(s_worst) / (np.array(s_worst) + np.array(s_best))

            df['Topsis Score'] = pi
            df['Rank'] = df['Topsis Score'].rank(ascending=False)

            df.to_csv(output_file, index=False)

        else:
            raise FileNotFoundError

    except FileNotFoundError:
        print('Error: File not found!')
    except ValueError as ve:
        print(f'Error: {str(ve)}')


def main():
    try:
        # Extract input arguments
        input_file = sys.argv[1]
        weights = [float(w) for w in sys.argv[2].split(',')]
        impacts = sys.argv[3].split(',')
        output_file = sys.argv[4]

        # Run the TOPSIS algorithm
        topsis(input_file, weights, impacts, output_file)

    except ValueError as ve:
        print(f'Error: {str(ve)}')


if __name__ == "__main__":
    main()
