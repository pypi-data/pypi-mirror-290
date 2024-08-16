import pandas as pd
import numpy as np
import sys
import os

def check_inputs(weights, impacts, num_cols):
    if not isinstance(impacts, str) or not isinstance(weights, str):
        raise ValueError("Impacts and weights must be strings separated by commas.")
    
    impacts_list = impacts.split(',')
    weights_list = weights.split(',')
    
    if len(impacts_list) != len(weights_list) or len(impacts_list) != num_cols-1:
        raise ValueError("The number of impacts and weights must be the same.")
    
    for impact in impacts_list:
        if impact not in ['+', '-']:
            raise ValueError("Impacts must be either '+' or '-'.")

    try:
        weights_list = [float(weight) for weight in weights_list]
    except ValueError:
        raise ValueError("Weights must be numeric values.")
    
    return weights_list, impacts_list
    
    
def topsis( weights, impacts, input_file, output_file, ):
    try:
        if not os.path.exists(input_file):
            raise FileNotFoundError("Input File not found.")
    except FileNotFoundError as e:
        print(e)
        exit(1)
        
    
    df = pd.read_csv(input_file)
        
    if len(df.columns) < 3:
        raise ValueError("Input file must contain three or more columns.")
    
    weights, impacts = check_inputs(weights, impacts, len(df.columns))
    
    data = df.iloc[:, 1:].values
        
    den = np.sqrt(np.sum(data**2, axis=0))
    normal = data/den
    
    weighted = normal * weights
    
    best = np.zeros(weighted.shape[1])
    worst = np.zeros(weighted.shape[1])
    # impact = np.array(impacts)
    
    for i in range(weighted.shape[1]):
        if impacts[i]=="+":
            best[i] = np.max(weighted[:, i])
            worst[i] = np.min(weighted[:, i])
        else:
            best[i] = np.min(weighted[:, i])
            worst[i] = np.max(weighted[:, i])
            
    ds1 = np.sqrt(np.sum((weighted - best) ** 2, axis=1))     
    ds2 = np.sqrt(np.sum((weighted - worst) ** 2, axis=1))   
    
    total = ds1 + ds2
    performance = ds2/total
    
    df['Topsis Score'] = performance
    df['Rank'] = df['Topsis Score'].rank(ascending=False).astype(int)
    
    df.to_csv(output_file, index=False)
    
    print(f"Results saved to {output_file}")
    

def main():
    if len(sys.argv) != 5:
        print("Usage: python <program.py> <InputDataFile> <Weights>  <Impacts> <ResultFileName>")
        exit(1)
    
    input_file = sys.argv[1]
    weights = sys.argv[2]
    impacts = sys.argv[3]
    output_file = sys.argv[4]
        
    performance = topsis(input_file, weights, impacts, output_file)
    print(f"TOPSIS analysis complete. Results saved to {output_file}.")
    
if __name__ == "__main__":
    main()