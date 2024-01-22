#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np
import sys
def is_parameter_num_correct():
    if len(sys.argv)!=5:
        print("""Error-Not correct number of parameters it should be in the format 
              102103072.py <INPUTFILE> <WEIGHTS> <IMPACTS> <RESULTFILE>""")
        sys.exit(1)
def check_arguments(arg):
    if not arg[1].endswith('.csv') or not arg[4].endswith('.csv'):
        print("Error-First and last command line arguments should be a CSV file")
        sys.exit(1)
   
def check_and_load_data(inputfile):
    try:
        df=pd.read_csv(inputfile)
        return df
    except FileNotFoundError:
        print("Error-Your File {} is not found. Please Check for your file".format(inputfile))
        sys.exit(1)
def len_column_check(input_data):
    if len(input_data.columns) < 3:
        print("Error-Input_file must have at least 3 columns")
        sys.exit(1)
def is_numeric(input_data):
    numeric_columns = input_data.iloc[:,1:].select_dtypes(include=['number'])
    if not numeric_columns.equals(input_data.iloc[:,1:]):
        print("Error-There should be only numeric values from 2nd column to last column")
        sys.exit(1)
def number_weight_impact_col_check(input_data,weights,impacts):
    if len(weights) != len(impacts):
        print("Error-Number of weights, number of impacts and number of columns (from 2nd to last columns) must be same.")
        sys.exit(1)
    elif len(weights) != len(input_data.columns) - 1:
        print("Error-Weights and Inputs are not equal to number of columns (from 2nd to last columns).These 3 must be same.")
        sys.exit(1)
def impact_check(impacts):
    for impact in impacts:
        if impact not in ['+','-']:
            print("Error-Impact should be either + or -")
            sys.exit(1)
def impact_weight_sep_check(impacts,weights,n,m):
    impacts_split = impacts.split(',')
    weights_split = weights.split(',')

    if len(impacts_split) == 1:
        print("Error: Impacts not separated by ,")
        sys.exit(1)
    if len(weights_split) == 1:
        print("Error: Weights not separated by ,")
        sys.exit(1)
    

def topsis(input_data, weights, impacts):
    col=input_data.iloc[:,1:]
    normalized_data = col.apply(lambda x: x/np.sqrt(np.sum(x**2)),axis=0)
    weighted_data = normalized_data * weights
    ideal_best = []
    ideal_worst = []
    for i,impact in zip(weighted_data.columns,impacts):
        if impact == '+':
            ideal_best.append(weighted_data[i].max())
            ideal_worst.append(weighted_data[i].min())                      
        elif impact == '-':
            ideal_best.append(weighted_data[i].min())
            ideal_worst.append(weighted_data[i].max())     
                               
    s_positive = np.linalg.norm(weighted_data - ideal_best, axis=1)
    s_negative =  np.linalg.norm(weighted_data - ideal_worst, axis=1)
    topsis_score = s_negative / (s_negative + s_positive)
    input_data['Topsis Score'] = topsis_score
    rank = input_data['Topsis Score'].rank(ascending=False).astype(int)
    input_data['Rank'] = rank.astype(int)

def main():
    is_parameter_num_correct()
    check_arguments(sys.argv)
    input_data = sys.argv[1]
    input_data = check_and_load_data(input_data)
    len_column_check(input_data)
    is_numeric(input_data)
    w = sys.argv[2].split(',')
    impacts = sys.argv[3].split(',')
    impact_weight_sep_check(sys.argv[3], sys.argv[2], len(input_data.columns) - 1, len(input_data.columns) - 1)
    impact_check(impacts)

    number_weight_impact_col_check(input_data, w, impacts)
    weights = [int(w) for w in w]

    output_file = sys.argv[4]
    topsis(input_data, weights, impacts)
    try:
        input_data.to_csv(output_file, index=False)
        print("Output file: {} is written successfully".format(output_file))
    except Exception as e:
        print(f"Error writing to the file: {e}")
    print(input_data)

if __name__ == "__main__":
    main()
           
    
    




