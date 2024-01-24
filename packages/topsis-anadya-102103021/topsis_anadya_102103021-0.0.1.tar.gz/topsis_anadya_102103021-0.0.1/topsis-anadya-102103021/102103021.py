def main():
    import pandas as pd
    import numpy as np 

    dataFile=str(input('InputDataFile'))
    data=pd.read_csv(dataFile)

    df=data[["P1","P2","P3","P4","P5"]]

    ans=df.apply(lambda x: (np.sum(x*x)),0)
    ans=np.sqrt(ans)
    norm=df.apply(lambda x:x/ans,1)

    w=input("Weights")
    w=w.split(sep=',')
    weights=[]
    for i in w:
        weights.append(float(i))
    x=sum(weights)
    for i in range(0,len(weights)):
        weights[i]=weights[i]/x

    w_norm=norm.apply(lambda x:x*weights,1)

    best=w_norm.max(0)
    worst=w_norm.min(0)

    impact=input("Impacts")
    impacts=impact.split(',')

    sPlus=w_norm.apply(lambda x: ((x-best)*(x-best)),1).sum(1)
    sMinus=w_norm.apply(lambda x: ((x-worst)*(x-worst)),1).sum(1)
    w_norm["S+"]=sPlus
    w_norm["S-"]=sMinus

    perf=w_norm["S-"]/(w_norm["S+"]+w_norm["S-"])
    w_norm["P"]=perf

    mod=np.arange(0,8)
    w_norm["Model"]=mod
    w_norm=w_norm.sort_values("P",ascending=False)
    w_norm["Rank"]=np.arange(1,9)
    w_norm=w_norm.sort_values("Model")
    result=data
    result["Topsis Score"]=w_norm["P"]
    result["Rank"]=w_norm["Rank"]
    FileName=str(input("ResultFileName"))
    result.to_csv(FileName)

if __name__=='102103021':
    main()