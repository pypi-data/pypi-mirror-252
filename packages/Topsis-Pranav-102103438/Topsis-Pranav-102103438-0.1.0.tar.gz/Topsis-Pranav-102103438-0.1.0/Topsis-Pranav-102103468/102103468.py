import pandas as pd
import numpy as np
import os

def is_numeric(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def topsis(data, weights,impacts):
  
    normalized_matrix = data / np.linalg.norm(data, axis=0)

    weighted_matrix = normalized_matrix * weights

    ideal_best = np.max(weighted_matrix, axis=0) if impacts =='+' else np.min(weighted_matrix, axis=0)
    ideal_worst = weighted_matrix.min() if impacts == '+' else np.max(weighted_matrix, axis=0)
    best_dist = np.linalg.norm(weighted_matrix - ideal_best, axis=1)
    worst_dist = np.linalg.norm(weighted_matrix - ideal_worst, axis=1)

    performance_scores = worst_dist / (best_dist + worst_dist)
    
    rankings = np.argsort(performance_scores) + 1
    return performance_scores, rankings

def topsis_from_csv(input_csv,output_csv,weights,impacts):
    try:
        df = pd.read_csv(input_csv)
        
        if len(df.columns) < 3:
            raise ValueError("Input CSV must have at least 3 columns")
        
        for col in df.columns[1:]:
            if not all(df[col].apply(is_numeric)):
                raise ValueError(f"Column '{col}' must contain numeric values only.")
            
        if len(weights) != len(impacts) or len(weights) != len(df.columns) - 1:
            raise ValueError("Number of weights, impacts, and columns must be the same.")
                
        if not all(impact in ['+', '-'] for impact in impacts):
            raise ValueError("Impacts must be either + or -.")
        decision_matrix = df.iloc[:,1:].values
        scores,rankings = topsis(decision_matrix,weights,impacts)
        
        df['Topsis Score'] = scores
        df['Rank'] = rankings
        
        if not os.path.exists(output_csv):
            df.to_csv(output_csv, index=False)
        else:
            df.to_csv(output_csv, mode='a', header=False, index=False)
        print(f"TOPSIS results have been written to '{output_csv}'.")
    except FileNotFoundError:
        print(f"File '{input_csv}' not found.")
    except ValueError as e:
        print(f"Error: {str(e)}")   
    
    



read_file = pd.read_excel("data.xlsx")
read_file.to_csv("102103468-data.csv", index=None, header=True)
df = pd.DataFrame(pd.read_csv("102103468-data.csv"))
weights = [2, 2, 3, 3, 4]
impacts = ['-','+', '-', '+', '-']

print(df)

topsis_from_csv("102103468-data.csv","102103468-result.csv",weights,impacts)
df_result = pd.DataFrame(pd.read_csv("102103468-result.csv"))
print(df_result)