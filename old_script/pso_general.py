import numpy as np
from decimal import Decimal
from pyswarm import pso
import matplotlib.pyplot as plt
import math
import csv
import sys
import evaluation
from evaluation import *

print('CPCR Curve fitting')
print('  the function is a+b*x+c/((1+math.exp(-d*(x-e)))*(1+math.exp(-f*(x-g))))')
print('  the program use pso to optimze the parameter of fuction above')
# caculate mean of the data of experiment  
'''def caculatemean(arg,size):
    sum=0.0
    for i in xrange(size):
        sum=sum+arg[i]
    return sum/size
#caculate the  predict data using function 
def caculate(x,parameters):
    a,b,c,d,e,f,g=parameters
    return a+b*x+c/((1+math.exp(-d*(x-e)))*(1+math.exp(-f*(x-g))))
# score function R-score=-1+SSE/SST
def myfunction(parameters,*args):
    a,b,c,d,e,f,g=parameters
    y=args
    SSE=0.0
    size=len(y)
    parametersSize=len(parameters)
    for i in xrange(size):
        yi=caculate(i+1,parameters)
        SSE=SSE+math.pow((y[i]-yi),2)
    meanvalue=caculatemean(args,size)
    SST=0.0
    for i in xrange(size):
        SST=SST+math.pow((y[i]-meanvalue),2)
        if SST==0:
            print('warning the SST maybe be zero')
    SS=1-SSE/SST
    return (SSE/SST)-1     #R-score
    #return (parametersSize/(size-parametersSize-1))*(1-SS)-SS   #adjust R-score
    #return SSE
# prepare the csv format data of experiment'''
length=0
def SSE(parameters,*args):
    return SSEfunction(parameters,args,0,length)

def RMSE(parameters,*args):
    return RMSEfunction(parameters,args,0,length)

def RScore(parameters,*args):
    return R_score(parameters,args,0,length)

def AdjustRS(parameters,*args):
    return Adjusted_R_score(parameters,args,0,length)
def RMSE_RS(parameters,*args):
    return RMSEandRScore(parameters,args,0,length)
def readfile(filename):
    rows=[]
    with open(filename) as f:
        f_csv=csv.reader(f)
        headers=next(f_csv)
        for row in f_csv:
            if row:
                rows.append(row)
    return np.array(np.transpose(rows),dtype=float)
#caculate average of all number to shutdown the number 
def caculatemidnum(data):
    sum=0.0
    length=len(data)
    for itera in data:
        sum=sum+(itera)
    return sum/(length*60)
#caculate Maxnum num in every col
'''def caculateMaxNum(data):
    max=0
    for itera in data:
        if itera>max:
            max=itera
    return max/60.0'''
# produce iterations of pso according to the pcr data infomation
def constraint(data,length):
    sum=200
    for itera in xrange(1,length):
        if data[itera]<data[itera-1]:
            sum=sum+10
    return sum
# the main function of this program
def main():

    global length
    filename=sys.argv[1]
    function=sys.argv[2]
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
        iteration=constraint(args,length)
        print('iterations={}'.format(iteration))
        print("please wait a moment....")
        minNum=args.min()
        maxNum=args.max()
        meanNum=args.mean()
        lb=[-1,0,-meanNum,-1,-maxNum,-1,-maxNum]
        ub=[1,0.5,2*maxNum+meanNum,1.1,3*maxNum+meanNum,1.1,3*maxNum+meanNum]
        initialData=[0,0.01,meanNum,-1,maxNum,0.7,maxNum]
        initialData2=[0,0.03,maxNum,0.1,2*maxNum,-1,2*maxNum] 
        if function=="SSE": 
            xopt4,fopt4=pso(SSE,lb,ub,args=args,initialData=initialData,initialData2=initialData2,swarmsize=250,maxiter=iteration)
        elif function=="RMSE":
            xopt4,fopt4=pso(RMSE,lb,ub,args=args,initialData=initialData,initialData2=initialData2,swarmsize=250,maxiter=iteration)
        elif function=="REandRS":
            print("REandRS")
            xopt4,fopt4=pso(RMSE_RS,lb,ub,args=args,initialData=initialData,initialData2=initialData2,swarmsize=250,maxiter=iteration)
        elif function=="RScore":
            xopt4,fopt4=pso(RScore,lb,ub,args=args,initialData=initialData,initialData2=initialData2,swarmsize=250,maxiter=iteration)
        else:
            xopt4,fopt4=pso(AdjustRS,lb,ub,args=args,initialData=initialData,initialData2=initialData2,swarmsize=250,maxiter=iteration)
        print('The optimum is at:')
        print('    {}'.format(xopt4))
        print('Optimal function values:')
        #print('    R-square : {}'.format(fopt4))
        print('ajusted R-squared:{}'.format(-fopt4)) 
        file_result.write(repr(xopt4[0]).rjust(10)+repr(xopt4[1]).rjust(10)+repr(xopt4[2]).rjust(10)+repr(xopt4[3]).rjust(10)+repr(xopt4[4]).rjust(10)+repr(xopt4[5]).rjust(10)+repr(xopt4[6]).rjust(10)+repr(fopt4).rjust(10)+'\n')
        x=np.linspace(1,length,10000)
        y=xopt4[0]+xopt4[1]*x+xopt4[2]/((1+np.exp(-xopt4[3]*(x-xopt4[4])))*(1+np.exp(-xopt4[5]*(x-xopt4[6]))))
        plt.figure(rownum)
        for i in xrange(length):
            plt.plot(i+1,args[i],'blue',linestyle='dashed',marker='.')
        plt.plot(x,y,'r',linewidth=2)
        plt.xlabel("circle(Time)")
        plt.ylabel("fluorescence")
        plt.legend()
        plt.show()
    if row>0:
        file_result.close()
if __name__=="__main__":
    main()


    
