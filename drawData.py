import numpy as np
import matplotlib.pyplot as plt
import measure
from measure import *
import os
import sys

def main():
    plt.figure(1)
    plt.xlabel("circle(Time)")
    plt.ylabel("raw fluorescence")
    filename=sys.argv[1]
    filename2=sys.argv[2]
    data=readfile(filename)
    parameters=readfile(filename2)
    row,col=data.shape
    #print max(data[row-4])
    newbigger=[]
    for rownum in xrange(row):
         newbigger.append(data[rownum][col-1])
    midnum=caculatemidnum(newbigger)
    data=data/midnum
    if row>0:
        os.system("clear")
    for rownum in xrange(row):
        args=data[rownum]
        plt.figure(1)
        for i in xrange(col):
            plt.plot(i+1,args[i],marker='.')
    x=np.linspace(0,90,100)
    for rownum in xrange(row):
        xopt4=parameters[rownum]
        y=xopt4[0]+xopt4[1]*x+xopt4[2]/((1+np.exp(-xopt4[3]*(x-xopt4[4])))*(1+np.exp(-xopt4[5]*(x-xopt4[6]))))
        plt.figure(1) 
        plt.plot(x,y)


    plt.show()
if __name__=="__main__":
    main()
    
        

