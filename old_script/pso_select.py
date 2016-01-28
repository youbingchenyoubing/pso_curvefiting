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
    if row>0:
        file_result_itera=open('./result/result_select_itera.txt','w')
        file_result_itera.close()
        file_result=open('./result/result_select.txt','w')
        file_result.write(repr('para_a').rjust(40)+repr('para_b').rjust(40)+repr('para_c').rjust(40)+repr('para_d').rjust(40)+repr('para_e').rjust(40)+repr('para_f').rjust(40)+repr('para_g').rjust(40)+repr('error').rjust(40)+'\n')
    for rownum in xrange(row):
        '''print data[rownum].min()
        print data[rownum].max()
        print data[rownum].mean()'''
        args=data[rownum]
        length=len(args)
        maxPosition=getX(args,length)
        if maxPosition<30:
            Xmin=0
            Xmax=maxPosition+40-(maxPosition-Xmin)
        elif maxPosition>length-10:
            Xmax=length-1
            Xmin=maxPosition-40+(Xmax-maxPosition)
        else:
            Xmax=maxPosition+10
            Xmin=maxPosition-30
        iteration=constraint(args,Xmin,Xmax)
        print('iterations={}'.format(iteration))
        print('maxPosition={}'.format(maxPosition))
        minNum=args.min()
        maxNum=args.max()
        meanNum=args.mean()
        general=meanNum+maxNum
        radio=getArrange(args,length)/10
        radiomax=radio*maxNum
        radiomean=radio*meanNum
        lb=[-1,0,minNum,-1,0,-1,0]
        ub=[1,0.5,meanNum+radiomean,1.1,general+radiomax,1.1,general+radiomax]
        initialData=[0,0.01,meanNum,-1,maxNum,0.7,maxNum]
        initialData2=[0,0.03,meanNum,0.1,maxNum,-1,radiomax] 
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
        elif function=="RERS":
            xopt4,fopt4=pso(RMSE_RS,lb,ub,args=args,initialData=initialData,initialData2=initialData2,swarmsize=250,maxiter=iteration)
            print('Optimal function values:')
            print('1/2*RMSE+1/2*R-squared:{}'.format(-fopt4)) 
        else:
            xopt4,fopt4=pso(AdjustRS,lb,ub,args=args,initialData=initialData,initialData2=initialData2,swarmsize=250,maxiter=iteration)
            print('Optimal function values:')
            print('ajusted R-squared:{}'.format(-fopt4)) 
        file_result.write(repr(xopt4[0]).rjust(40)+repr(xopt4[1]).rjust(40)+repr(xopt4[2]).rjust(40)+repr(xopt4[3]).rjust(40)+repr(xopt4[4]).rjust(40)+repr(xopt4[5]).rjust(40)+repr(xopt4[6]).rjust(40)+repr(fopt4).rjust(40)+'\n')
        x=np.linspace(Xmin-2,Xmax+2,10000)
        y1=xopt4[0]+xopt4[1]*x+xopt4[2]/((1+np.exp(-xopt4[3]*(x-xopt4[4])))*(1+np.exp(-xopt4[5]*(x-xopt4[6]))))
        print('The optimum is at:')
        print('    {}'.format(xopt4))
        minimizefunction(xopt4,Xmin,Xmax,args)
        '''file_result.write(repr(xopt4[0]).rjust(40)+repr(xopt4[1]).rjust(40)+repr(xopt4[2]).rjust(40)+repr(xopt4[3]).rjust(40)+repr(xopt4[4]).rjust(40)+repr(xopt4[5]).rjust(40)+repr(xopt4[6]).rjust(40)+repr(fopt4).rjust(40)+'\n')
        y=xopt4[0]+xopt4[1]*x+xopt4[2]/((1+np.exp(-xopt4[3]*(x-xopt4[4])))*(1+np.exp(-xopt4[5]*(x-xopt4[6]))))
        plt.figure(rownum)
        for i in xrange(Xmin,Xmax):
            plt.plot(i+1,args[i],'blue',linestyle='dashed',marker='.')
        plt.plot(x,y1,'y',linewidth=2)
        plt.plot(x,y,'r',linewidth=2)
        plt.plot(maxPosition,args[maxPosition-1],'red',linestyle='dashed',marker='*')
        plt.xlabel("circle(Time)")
        plt.ylabel("fluorescence")
        plt.legend()
        plt.show()'''
    if row>0:
        file_result.close()
        print("***********************attention************************************")
        print("please go to the dir of result to save this result_select.txt and result_select_itera.txt\n")
if __name__=="__main__":
    main()


    
