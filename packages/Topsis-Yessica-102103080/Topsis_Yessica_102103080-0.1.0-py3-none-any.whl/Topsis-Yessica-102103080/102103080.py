#!/usr/bin/env python
# coding: utf-8

# In[1]:


def TOPSIS(inpt, wt, sn, oupt):
    import math as mt
    import numpy as np
    import pandas as pd
    sq=[]
    Vp=[]
    Vn=[]
    Sp=[]
    Sn=[]
    try:
        df = pd.read_csv(inpt)
    except FileNotFoundError:
        return f"Error: Incorrect File"
    num = wt.split(',')
    wgt =[n.strip() for n in num]
    for i in range(len(wgt)):
        wgt[i]=float(wgt[i])
    sign = sn.split(',')
    sgn =[g.strip() for g in sign]
    arr = df.values.T
    v1=arr[1:]
    v2=np.zeros_like(v1)
    for i in range(len(v2)):
        for j in range(len(v2[i])):
            x=v1[i][j]
            v2[i][j]=x**2
        y=sum(v2[i])
        y=mt.sqrt(y)
        sq.append(y)
        v1[i]=(v1[i]/sq[i])*wgt[i]
    for i in range(len(v1)):
        M=max(v1[i])
        m=min(v1[i])
        if sgn[i]=="+":
            Vp.append(M)
            Vn.append(m)
        else:
            Vp.append(m)
            Vn.append(M)
    v3=v1.T
    for i in range (len(v3)):
        a = sum((x - y) ** 2 for x, y in zip(v3[i], Vp))
        Sp.append(mt.sqrt(a))
        b = sum((x - y) ** 2 for x, y in zip(v3[i], Vn))
        Sn.append(mt.sqrt(b))
    Ssum=np.add(Sp, Sn)
    pf=np.divide(Sn,Ssum)
    er = {r: rank for rank, r in enumerate(sorted(pf, reverse=True), start=1)}
    order = [er[r] for r in pf]
    df['Performance score']=pf
    df['Rank']=order
    df.to_csv(oupt, index=False)
    return "File saved Successfully"


# In[2]:


def main():
    import sys
    if len(sys.argv) != 5:
        sys.exit(1)

    inpt, wt, sn, oupt = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    result = topsis(inpt, wt, sn, oupt)
    print(result)

if __name__ == "__main__":
    main()


# In[ ]:




