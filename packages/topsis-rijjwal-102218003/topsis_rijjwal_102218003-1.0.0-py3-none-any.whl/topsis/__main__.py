import sys
import numpy as np
import pandas as pd


def topsis(data,weights,impact):
    
    deno=np.sqrt(np.sum((data)**2,axis=0))
    norm=data/deno
    
    
    weighted_data = norm * weights
    
   
    best=np.zeros(weighted_data.shape[1])
    worst=np.zeros(weighted_data.shape[1])
    impact=np.array(impact)
    for i in range(weighted_data.shape[1]):
        if impact[i]=="+":
            best[i]=np.max(weighted_data[:,i])
            worst[i]=np.min(weighted_data[:,i])
        else:
            best[i]=np.min(weighted_data[:,i])
            worst[i]=np.max(weighted_data[:,i])
 
 
    dist1 = np.sqrt(np.sum((weighted_data - best) ** 2, axis=1)) 
    dist2 = np.sqrt(np.sum((weighted_data - worst) ** 2, axis=1)) 
    
    
    total=dist1+dist2 
    performance=dist2/total
    
    return performance
    
        


def main():
    if(len(sys.argv)!=5):
        print("PLEASE TYPE CORRECT INPUT")
        sys.exit(1)
    input_file=sys.argv[1]
    data=pd.read_csv(input_file)
    df=data.drop(data.columns[0],axis=1)
    
    impacts=sys.argv[3].split(',')
    weights = list(map(float, sys.argv[2].split(','))) 
    
    performance=topsis(df.to_numpy(),weights,impacts)
    
    data['Topsis Score'] = performance
    
    data['Rank'] = data['Topsis Score'].rank(method='max', ascending=False).astype(int)
    
    output_file=sys.argv[4]
    
    data.to_csv(output_file, index=False)
    print("RESULT FILE UPDATED") 
    
    
if __name__=="__main__":
    main()   