import numpy as np
from decimal import Decimal
from pyswarm import pso
import matplotlib.pyplot as plt
import math
import csv
import sys
print('attention****this script is for general data')
print('CPCR Curve fitting')
print('  the function is a+b*x+c/((1+math.exp(-d*(x-e)))*(1+math.exp(-f*(x-g))))')
print('  the program use pso to optimze the parameter of fuction above')
def caculatemean(arg,size):
    sum=0.0
    for i in xrange(size):
        sum=sum+arg[i]
    return sum/size
def caculate(x,parameters):
    a,b,c,d,e,f,g=parameters
    return a+b*x+c/((1+math.exp(-d*(x-e)))*(1+math.exp(-f*(x-g))))
def myfunction(parameters,*args):
    a,b,c,d,e,f,g=parameters
    y=args
    SSE=0.0
    size=len(y)
    for i in xrange(size):
        yi=caculate(i+1,parameters)
        SSE=SSE+math.pow((y[i]-yi),2)
    meanvalue=caculatemean(args,size)
    SST=0.0
    for i in xrange(size):
        SST=SST+math.pow((y[i]-meanvalue),2)
        if SST==0:
            print('warning the SST maybe be zero')
    return (SSE/SST)-1

def readfile(filename):
    rows=[]
    with open(filename) as f:
        f_csv=csv.reader(f)
        headers=next(f_csv)
        for row in f_csv:
            if row:
                rows.append(row)
    return np.array(np.transpose(rows),dtype=float)
def caculatemidnum(data):
    sum=0.0
    length=len(data)
    for itera in data:
        sum=sum+(itera)
    return sum/(length*60)
def main():


    filename=sys.argv[1]
    data=readfile(filename)
    row,col=data.shape
    #print max(data[row-4])
    newbigger=[]
    for rownum in xrange(row):
         newbigger.append(data[rownum][col-1])
    midnum=caculatemidnum(newbigger)
    data=data/midnum
    if row>0:
        file_result=open('result.txt','w')
        file_result.write(repr('para_a').rjust(10)+repr('para_b').rjust(10)+repr('para_c').rjust(10)+repr('para_d').rjust(10)+repr('para_e').rjust(10)+repr('para_f').rjust(10)+repr('para_g').rjust(10)+repr('error').rjust(10)+'\n')
    for rownum in xrange(row):
        '''print data[rownum].min()
        print data[rownum].max()
        print data[rownum].mean()'''
        args=data[rownum]
        length=len(args)
        minNum=args.min()
        maxNum=args.max()
        meanNum=args.mean()
        lb=[minNum,0,meanNum-100,-1,maxNum-100,-1,maxNum-100]
        ub=[meanNum,0.5,meanNum+maxNum,1.1,meanNum+maxNum,1.1,meanNum+maxNum]
        initialData=[minNum,0.01,meanNum,0.1,maxNum,0.7,maxNum]
        initialData2=[minNum,0.03,meanNum,0.1,maxNum,-1,maxNum] 
        xopt4,fopt4=pso(myfunction,lb,ub,args=args,initialData=initialData,initialData2=initialData2)
        print('The optimum is at:')
        print('    {}'.format(xopt4))
        print('Optimal function values:')
        print('    weight         : {}'.format(-fopt4))
        file_result.write(repr(xopt4[0]).rjust(10)+repr(xopt4[1]).rjust(10)+repr(xopt4[2]).rjust(10)+repr(xopt4[3]).rjust(10)+repr(xopt4[4]).rjust(10)+repr(xopt4[5]).rjust(10)+repr(xopt4[6]).rjust(10)+repr(fopt4).rjust(10)+'\n')
        x=np.linspace(1,length,10000)
        y=xopt4[0]+xopt4[1]*x+xopt4[2]/((1+np.exp(-xopt4[3]*(x-xopt4[4])))*(1+np.exp(-xopt4[5]*(x-xopt4[6]))))
        plt.figure(rownum)
        for i in xrange(length):
            plt.plot(i+1,args[i],'blue',linestyle='dashed',marker='*')
        plt.plot(x,y,'r',linewidth=2)
        plt.xlabel("circle(Time)")
        plt.ylabel("Volt")
        plt.legend()
        plt.show()
    if row>0:
        file_result.close()
if __name__=="__main__":
    main()

