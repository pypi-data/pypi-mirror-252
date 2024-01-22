import sys
import numpy as np
import pandas as pd

def check_input():
    if len(sys.argv)!=5:
        print("Please enter 5 variables in the format of:- python <program.py> <InputDataFile> <Weights> <Impacts> <ResultFileName>")
        sys.exit(1)

def load_data(input_data):
    try:
        data= pd.read_csv(input_data)
        return data
    except FileNotFoundError:
        print('File not found \ntry again')
        sys.exit(1)

def check_input_data(data):
    if len(data.columns)<3:
        print("Error: Input file must contain three or more columns.")
        sys.exit(1)

    for col in data.columns[1:]:
        if not pd.to_numeric(data[col],errors='coerce').notna().all():
            print("Columns from 2nd to last must contain numeric values only.")
            sys.exit(1)

def check_weight_impact(data,weights,impacts):
    if len(weights)!= len(data.columns)-1 or len(impacts)!= len(data.columns)-1:
        print('Number of weights, impacts, and columns must be the same.')
        sys.exit(1)

    correct_impacts=set(['+','-'])
    if not set(impacts).issubset(correct_impacts):
        print('impacts can be + or -')
        sys.exit(1)

def normalize_data(data):
    normalized_data= data.copy()
    for col in data.columns[1:]:
        normalized_data[col]=data[col]/np.linalg.norm(data[col].values)
    return normalized_data

def calc_topsis(normalized_data,weights,impacts):
    ideal_best = np.max(normalized_data) if impacts == '+' else np.min(normalized_data)
    ideal_worst = np.min(normalized_data) if impacts == '+' else np.max(normalized_data)

    topsis_score=np.zeros(len(normalized_data))
    s_best=np.zeros(len(normalized_data))
    s_worst=np.zeros(len(normalized_data))
    for i in range(len(normalized_data)):
        s_best[i]=np.sqrt(np.sum((weights*normalized_data.iloc[i])-ideal_best)**2)
        s_worst[i]=np.sqrt(np.sum((weights*normalized_data.iloc[i])-ideal_worst)**2)
        topsis_score[i]= s_worst[i]/(s_best[i]+s_worst[i])

    return topsis_score

def rank_data(topsis_score):
    rank = len(topsis_score) - np.argsort(topsis_score).argsort()
    return rank

def main():
    check_input()
    input_file=sys.argv[1]
    weights = np.array(list(map(int, sys.argv[2].split(','))))
    impacts = sys.argv[3].split(',')
    result_file = sys.argv[4]

    data= load_data(input_file)
    check_input_data(data)
    check_weight_impact(data,weights,impacts)

    normalized_data=normalize_data(data)
    topsis_score=calc_topsis(normalized_data.iloc[:,1:],weights,impacts)
    data['Topsis Score'] = topsis_score
    data['Rank'] = rank_data(topsis_score)

    data.to_csv(result_file, index=False)
    print(f"Results saved to {result_file}")

if __name__=='__main__':
    main()



