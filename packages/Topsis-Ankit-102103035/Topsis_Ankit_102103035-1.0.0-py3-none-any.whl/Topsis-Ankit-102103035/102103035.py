#!/usr/bin/env python
# coding: utf-8

# In[17]:


def Topsis(inp, w, s, opt):
    import pandas as pd
    import numpy as np
    import math as mt
    try:
        df = pd.read_csv(inp)
    except FileNotFoundError:
        return f"Error: Input file '{inp}' not found."
    elements = w.split(',')
    wt =[element.strip() for element in elements]
    for i in range(len(wt)):
        wt[i]=float(wt[i])
    elements = s.split(',')
    sg =[element.strip() for element in elements]
    cols = df.values.T
    val1=cols[1:]
    val2=np.zeros_like(val1)
    for i in range(len(val1)):
        for j in range(len(val1[i])):
            x=val1[i][j]
            val2[i][j]=x**2
    sumsq=[]
    for i in range (len(val2)):
        x=sum(val2[i])
        sumsq.append(x)
    for i in range (len(sumsq)):
        sumsq[i]=mt.sqrt(sumsq[i])
    for i in range(len(val1)):
        val1[i]=(val1[i]/sumsq[i])*wt[i]
    vjp=[]
    for i in range(len(val1)):
        if sg[i]=="+":
            m=max(val1[i])
            vjp.append(m)
        else:
            m=min(val1[i])
            vjp.append(m)
    vjn=[]
    for i in range(len(val1)):
        if sg[i]=="+":
            m=min(val1[i])
            vjn.append(m)
        else:
            m=max(val1[i])
            vjn.append(m)
    val3=val1.T
    stp=[]
    stn=[]
    for i in range (len(val3)):
        x = sum((a - b) ** 2 for a, b in zip(val3[i], vjp))
        stp.append(mt.sqrt(x))
        y = sum((a - b) ** 2 for a, b in zip(val3[i], vjn))
        stn.append(mt.sqrt(y))
    stsum=np.add(stp, stn)
    per=np.divide(stn,stsum)
    erank = {e: rank for rank, e in enumerate(sorted(per, reverse=True), start=1)}
    rank = [erank[e] for e in per]
    df['TOPSIS Score']=per
    df['TOPSIS Rank']=rank
    df.to_csv(opt, index=False)
    return "File saved at output location"
                 


# In[ ]:


def main():
    import sys
    if len(sys.argv) != 5:
        print("Usage: python -m your_package.topsis input.csv weights criteria output.csv")
        sys.exit(1)

    inp, w, s, opt = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    result = topsis(inp, w, s, opt)
    print(result)

if __name__ == "__main__":
    main()

