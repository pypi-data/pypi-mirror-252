import argparse
import sys
import pandas as pd
import numpy as np

def loadData(filename):
    try:
        data = pd.read_csv(filename, encoding = 'ANSI')
        return data
    except FileNotFoundError:
        print("File not found.")
        sys.exit(1)

def main():
    #parser = argparse.ArgumentParser()
    #parser.add_argument("fileName")
    #parser.add_argument("weights")
    #parser.add_argument("impacts")
    #parser.add_argument("outFileName")

    #args = parser.parse_args()
    
    #no of args check
    if (len(sys.argv) != 5):
        print("Wrong format of args.")
        sys.exit(1)
        
    #check file exists
    data = loadData(sys.argv[1])
    
    #check columns
    if len(data.columns) < 3:
        print("Insufficient number of columns.")
        sys.exit(1)
    
    #check numerical
    non_numeric_bool = data.iloc[:, 1:].applymap(lambda x: not np.isreal(x)).any()
    if non_numeric_bool.any():
        print("Values from 2nd to last column must be numeric only.")
        sys.exit(1)
        
    #check weights, impacts
    if (',' not in sys.argv[2] or ',' not in sys.argv[3]):
        print("Weights and impacts must be seperated by commas.")
        sys.exit(1)
        
    weights = list(map(int, sys.argv[2].split(',')))
    impacts = sys.argv[3].split(',')
    numOfCols = len(data.columns)
    
    if (len(weights) != numOfCols - 1 or len(weights) != len(impacts)):
        print("Number of weights, impacts and numeric columns is different, they must be equal.")
        sys.exit(1)
        
    if not all(i in ['+', '-'] for i in impacts):
        print("Impacts must be of the format '+' or '-' only.")
        sys.exit(1)
        
    #topsis - normalize data
    normalizedData = data.iloc[:, 1:].applymap(lambda x: x / np.sqrt(np.sum(x**2)))
    weightedND = normalizedData * weights
    idealBest = []
    idealWorst = []
    for i in range(numOfCols - 1):
        if impacts[i] == '+':
            idealBest.append(weightedND.iloc[:, i].max())
            idealWorst.append(weightedND.iloc[:, i].min())
        else:
            idealBest.append(weightedND.iloc[:, i].min())
            idealWorst.append(weightedND.iloc[:, i].max())
            
    distB = np.sqrt(np.sum((weightedND - idealBest) ** 2))
    distW = np.sqrt(np.sum((weightedND - idealWorst) ** 2))
    
    topsisScore = distW / (distB + distW)
    
    data["Topsis Score"] = topsisScore
    data["Rank"] = data["Topsis Score"].rank(ascending = False)
    data.to_csv(sys.argv[4], index = False)
    print("Topsis implementation by Sahil Manchanda")
    print("Roll number: 102103134")
    print("Results saved to: ", sys.argv[4])
    
if __name__ == "__main__":
    main()