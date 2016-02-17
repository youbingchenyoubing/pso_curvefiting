import numpy as np
from decimal import Decimal
from pyswarm import pso
import matplotlib.pyplot as plt
import math
import csv
import sys
import os
import evaluation
from evaluation import *
import measure
from measure import *
print('CPCR Curve fitting')
print('  the function is a+b*x+c/((1+math.exp(-d*(x-e)))*(1+math.exp(-f*(x-g))))')
print('  the program use pso to optimze the parameter of fuction above')
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

# prepare the csv format data of experiment'''
def main():

    global length
    filename=sys.argv[1]
    RMSE=float(sys.argv[2])
    #function=sys.argv[2] 
    #method=sys.argv[3]
    data=readfile(filename)
    row,col=data.shape
    #print max(data[row-4])
    newbigger=[]
    for rownum in xrange(row):
         newbigger.append(data[rownum][col-1])
    midnum=caculatemidnum(newbigger)
    data=data/midnum
    if row>0:
        os.system("clear")
        #file_result_itera=open('./result/result_all_itera.txt','w')
        #file_result_itera.close()
        #file_result=open('./result/result_all.txt','w')
        #file_result.write(repr('para_a').rjust(40)+repr('para_b').rjust(40)+repr('para_c').rjust(40)+repr('para_d').rjust(40)+repr('para_e').rjust(40)+repr('para_f').rjust(40)+repr('para_g').rjust(40)+repr('error').rjust(40)+'\n')
    SST=[]
    for rownum in xrange(row):
        '''print data[rownum].min()
        print data[rownum].max()
        print data[rownum].mean()'''
        args=data[rownum]
        length=len(args)
        SSTone=SSTfunction([],args,0,length)
        SST.append(SSTone)
    SUMSST=0
    for colnum in xrange(row):
        SUMSST+=SST[colnum]
    TSS=SUMSST/row
    SSE=math.pow(RMSE,2)*col
    RScore=1-(SSE/TSS)
    print("Rscore={}".format(RScore))
    '''
        iteration=constraint(args,0,length-1)
        print('iterations={}'.format(iteration))
        minNum=args.min()
        maxNum=args.max()
        meanNum=args.mean()
        #general=maxNum
        radio=getX(args,length)
        Xmin,Xmax=getMinMax(length,radio)
        quick_sort(array,0,length-1)
        initial_a=array[2]
        initial_g=array[length-3]
        lb=[minNum,0,meanNum,-1,Xmin,-1,Xmin]
        ub=[meanNum,0.5,maxNum,1.1,Xmax,1.1,Xmax]
        initialData=[initial_a,0.01,initial_g-initial_a,-1,radio,0.7,radio]
        initialData2=[initial_a+1,0.03,initial_g-initial_a+2,0.1,radio,-1,radio] 
        print("please wait a moment....")
        if function=="SSE": 
            xopt4,fopt4=pso(SSE,lb,ub,args=args,initialData=initialData,initialData2=initialData2,swarmsize=250,maxiter=iteration,minstep=1e-12,minfunc=1e-12)
            print('Optimal function values:')
            print('SSE:{}'.format(fopt4)) 
        elif function=="RMSE":
            xopt4,fopt4=pso(RMSE,lb,ub,args=args,initialData=initialData,initialData2=initialData2,swarmsize=250,maxiter=iteration,minstep=1e-12,minfunc=1e-12)
            print('Optimal function values:')
            print('RMSE:{}'.format(-fopt4)) 
        elif function=="RScore":
            xopt4,fopt4=pso(RScore,lb,ub,args=args,initialData=initialData,initialData2=initialData2,swarmsize=250,maxiter=iteration,minstep=1e-12,minfunc=1e-12)
            print('Optimal function values:')
            print(' R-squared:{}'.format(-fopt4)) 
        elif function=="RERS":
            xopt4,fopt4=pso(RMSE_RS,lb,ub,args=args,initialData=initialData,initialData2=initialData2,swarmsize=250,maxiter=iteration,minstep=1e-12,minfunc=1e-12)
            print('Optimal function values:')
            print('1/2*RMSE+1/2*R-squared:{}'.format(-fopt4)) 
        else:
            xopt4,fopt4=pso(AdjustRS,lb,ub,args=args,initialData=initialData,initialData2=initialData2,swarmsize=250,maxiter=iteration,minstep=1e-12,minfunc=1e-12)
            print('Optimal function values:')
            print('ajusted R-squared:{}'.format(-fopt4)) 
        file_result.write(repr(xopt4[0]).rjust(40)+repr(xopt4[1]).rjust(40)+repr(xopt4[2]).rjust(40)+repr(xopt4[3]).rjust(40)+repr(xopt4[4]).rjust(40)+repr(xopt4[5]).rjust(40)+repr(xopt4[6]).rjust(40)+repr(fopt4).rjust(40)+'\n')
        print('The optimum is at:')
        print('    {}'.format(xopt4))
        print('please wait a moment again,it\'s next to minimize the function')
        fitfunction(xopt4,length,args,method=method)
    if row>0:
        file_result.close()
        print("***********************attention************************************")
        print('please go to dir of result to save result_all.txt file and result_all_itera.txt')'''
if __name__=="__main__":
    main()


    
