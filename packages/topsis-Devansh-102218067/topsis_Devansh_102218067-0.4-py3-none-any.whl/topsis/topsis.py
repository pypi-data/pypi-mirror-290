import numpy as np
import pandas as pd
import argparse
import sys
from scipy.stats import rankdata

def topsis(weights, impacts, infile, oufile):
    try:
        df = pd.read_csv(infile)
    except FileNotFoundError:
        print(f"Error: File '{infile}' not found!!")
        sys.exit(1)

    data = df.iloc[:, 1:]

    if not np.issubdtype(data.to_numpy().dtype, np.number):
        print("Error: All columns must be numeric!!")
        sys.exit(1)

    if len(weights) != len(impacts) or len(weights) != data.shape[1]:
        print("Error: The number of weights, impacts, and columns are not equal!!")
        sys.exit(1)

    if not all(i in ['+', '-'] for i in impacts):
        print("Error: Impacts must be either '+' or '-'.")
        sys.exit(1)

    norm_data = data / np.sqrt((data**2).sum(axis=0))
    ndata = norm_data * np.array(weights)

    i_best = np.where(np.array(impacts) == '+', ndata.max(axis=0), ndata.min(axis=0))
    i_worst = np.where(np.array(impacts) == '+', ndata.min(axis=0), ndata.max(axis=0))

    d_best = np.sqrt(((ndata - i_best)**2).sum(axis=1))
    d_worst = np.sqrt(((ndata - i_worst)**2).sum(axis=1))
    t_score = d_worst / (d_best + d_worst)

    ranks = rankdata(-t_score, method='min')
    
    df["Topsis Score"] = t_score
    df["Rank"] = ranks

    df.to_csv(oufile, index=False)

    return t_score, ranks

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("weights", type=str)
    parser.add_argument("impacts", type=str)
    parser.add_argument("inputfile", type=str)
    parser.add_argument("outputfile", type=str)

    args = parser.parse_args()

    try:
        weights = [float(w) for w in args.weights.split(',')]
    except ValueError:
        print("Error: Weights must be numeric and separated by commas!!!")
        sys.exit(1)

    impacts = args.impacts.split(',')

    topsis(weights, impacts, args.inputfile, args.outputfile)

if __name__ == "__main__":
    main()
