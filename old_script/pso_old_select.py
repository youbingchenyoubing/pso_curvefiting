import numpy as np
from decimal import Decimal
from pyswarm import pso
import matplotlib.pyplot as plt
import math
import csv
import sys
import evaluation
from evaluation import *
import measure
from measure import *

print('CPCR Curve fitting')
print('  the function is a+b*x+c/((1+math.exp(-d*(x-e)))*(1+math.exp(-f*(x-g))))')
print('  the program use pso to optimze the parameter of fuction above')
# caculate mean of the data of experiment 
Xmin=0
Xmax=90

def SSE(parameters,*args):
    return SSEfunction(parameters,args,Xmin,Xmax)

def RMSE(parameters,*args):
    return RMSEfunction(parameters,args,Xmin,Xmax)

def RScore(parameters,*args):
    return R_score(parameters,args,Xmin,Xmax)

def AdjustRS(parameters,*args):
    return Adjusted_R_score(parameters,args,Xmin,Xmax)
def RMSE_RS(parameters,*args):
    return RMSEandRScore(parameters,args,Xmin,Xmax)
def main():
   
    global Xmax
    global Xmin 
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
    if row>0
        file_result=open('./result/result_select_2.txt','w')
        file_result.write(repr('para_a').rjust(10)+repr('para_b').rjust(10)+repr('para_c').rjust(10)+repr('para_d').rjust(10)+repr('para_e').rjust(10)+repr('para_f').rjust(10)+repr('para_g').rjust(10)+repr('error').rjust(10)+'\n')
    for rownum in xrange(row):
        '''print data[rownum].min()
        print data[rownum].max()
        print data[rownum].mean()'''
        args=data[rownum]
        length=len(args)
        maxPosition=getX(args,length)
        if maxPosition<10:
            Xmin=0
            Xmax=maxPosition+40-(maxPosition-Xmin)
        elif maxPosition>length-30:
            Xmax=length-1
            Xmin=maxPosition-40+(Xmax-maxPosition)
        else:
            Xmax=maxPosition+30
            Xmin=maxPosition-10
        iteration=constraint(args,Xmin,Xmax)
        print('iterations={}'.format(iteration))
        print('maxPosition={}'.format(maxPosition))
        minNum=args.min()
        maxNum=args.max()
        meanNum=args.mean()
        general=meanNum+maxNum
        radio=getArrange(args,length)/16
        radiomax=radio*maxNum
        radiomean=radio*meanNum
        lb=[-1,0,minNum,-1,0,-1,0]
        ub=[1,0.5,general+radiomean,1.1,general+radiomax,1.1,general+radiomax]
        initialData=[0,0.01,meanNum,-1,maxNum,0.7,maxNum]
        initialData2=[0,0.03,radiomean,0.1,radiomax,-1,radiomax] 
        '''lb=[minNum,0,minNum,-1,-meanNum,-1,-meanNum]
        ub=[1,0.5,maxNum,1.1,maxNum+meanNum,1.1,maxNum+meanNum]
        initialData=[0,0.01,meanNum,-1,maxNum,0.7,maxNum]
        initialData2=[0,0.03,meanNum+4,0.1,maxNum,-1,maxNum]''' 
        print("please wait a moment....")
        if function=="SSE": 
            xopt4,fopt4=pso(SSE,lb,ub,args=args,initialData=initialData,initialData2=initialData2,swarmsize=250,maxiter=iteration)
            print('Optimal function values:')
            print('SSE:{}'.format(fopt4)) 
        elif function=="RMSE":
            xopt4,fopt4=pso(RMSE,lb,ub,args=args,initialData=initialData,initialData2=initialData2,swarmsize=250,maxiter=iteration)
            print('Optimal function values:')
            print('RMSE:{}'.format(-fopt4)) 
        elif function=="RScore":
            xopt4,fopt4=pso(RScore,lb,ub,args=args,initialData=initialData,initialData2=initialData2,swarmsize=250,maxiter=iteration)
            print('Optimal function values:')
            print(' R-squared:{}'.format(-fopt4)) 
        elif function=="REandRS":
            xopt4,fopt4=pso(RMSE_RS,lb,ub,args=args,initialData=initialData,initialData2=initialData2,swarmsize=250,maxiter=iteration)
            print('Optimal function values:')
            print('1/2*RMSE+1/2*R-squared:{}'.format(-fopt4)) 
        else:
            xopt4,fopt4=pso(AdjustRS,lb,ub,args=args,initialData=initialData,initialData2=initialData2,swarmsize=250,maxiter=iteration)
            print('Optimal function values:')
            print('ajusted R-squared:{}'.format(-fopt4)) 
        print('The optimum is at:')
        print('    {}'.format(xopt4))
        file_result.write(repr(xopt4[0]).rjust(10)+repr(xopt4[1]).rjust(10)+repr(xopt4[2]).rjust(10)+repr(xopt4[3]).rjust(10)+repr(xopt4[4]).rjust(10)+repr(xopt4[5]).rjust(10)+repr(xopt4[6]).rjust(10)+repr(fopt4).rjust(10)+'\n')
        x=np.linspace(Xmin,Xmax,10000)
        y=xopt4[0]+xopt4[1]*x+xopt4[2]/((1+np.exp(-xopt4[3]*(x-xopt4[4])))*(1+np.exp(-xopt4[5]*(x-xopt4[6]))))
        plt.figure(rownum)
        for i in xrange(Xmin,Xmax):
            plt.plot(i+1,args[i],'blue',linestyle='dashed',marker='.')
        plt.plot(x,y,'r',linewidth=2)
        plt.plot(maxPosition,args[maxPosition-1],'red',linestyle='dashed',marker='*')
        plt.xlabel("circle(Time)")
        plt.ylabel("fluorescence")
        plt.legend()
        plt.show()
    if row>0:
        file_result.close()
if __name__=="__main__":
    main()


    
