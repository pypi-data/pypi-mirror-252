
import sys
import os
import copy
import math
import pandas as pd
import numpy as np
from os import path

def topsis(source1,weight,impact,dest1):
  
    class myexception(Exception):
          pass
    source=source1
    dest=dest1
    if not (path.exists(source)):
        raise myexception("No such file exists")
    if not source.endswith('.csv'):
        raise myexception("Enter CSV format file only")
        
    df1=pd.read_csv(source1)
    col=df1.shape
    if not col[1]>=3:
        raise myexception("Input file must contain 3 or more columns")
   
    k=0
    for i in df1.columns:
        k=k+1
        for j in df1.index:
            if k!=1:
                val=isinstance(df1[i][j],int)
                val1=isinstance(df1[i][j],float)
                if not val and not val1:
                    raise myexception("Values are not numeric")
                    
    w=[]
    wt=weight.split(',')
    for i in wt:
        k=0
        for j in i:
            if not j.isnumeric():
                if k>=1 or j!='.':
                    raise myexception("Format of Weight is not correct")
                else:
                    k=k+1
        w.append(float(i))

    if len(wt)!=(col[1]-1):
        raise myexception("Number of weight and number of columns must be equal")
        
    imp=impact.split(',')
    for i in imp:
        if i not in {'+','-'}:
            raise myexception("Format of impact is not correct")
    if len(imp)!=col[1]-1:
        raise myexception("Number of impact and Number of columns must be equal")


    df=copy.deepcopy(df1)
    df.drop(df.columns[[0]],axis=1,inplace=True)
    a=df.to_numpy()
    b=[]
    rows=len(a)
    columns=len(a[0])
    
    for i in range(columns): 
        b.append(math.sqrt(sum(a[:,i]*a[:,i])))
    normalised_a=[]
    for i in range(rows):
        a1=[]
        for j in range(columns):
            a1.append(a[i][j]/b[j]*w[j])
        normalised_a.append(a1)
    normalised_a=np.array(normalised_a)

    maximum=normalised_a.max(axis=0)
    minimum=normalised_a.min(axis=0)

    v_pos=[]
    v_neg=[]
    for i in range(columns):
        if imp[i] == '-':
            v_pos.append(minimum[i])
            v_neg.append(maximum[i])
        if imp[i]=='+':
            v_pos.append(maximum[i])
            v_neg.append(minimum[i])

    s_pos=[]
    s_neg=[]
    for i in range(rows):
        temp=0
        temp1=0
        for j in range(columns):
            temp+=(normalised_a[i][j]-v_pos[j])**2
            temp1+=(normalised_a[i][j]-v_neg[j])**2
        temp=temp**0.5
        temp1=temp1**0.5
        s_neg.append(temp1)
        s_pos.append(temp)

    spos_sneg=np.add(s_pos,s_neg)

    topsis_score=[]
    for i in range(rows):
        topsis_score.append(s_neg[i]/spos_sneg[i])

    df1['Topsis Score']=topsis_score
    df1["Rank"] = df1["Topsis Score"].rank(ascending=False) 

    df1.to_csv(dest1,index=False)

