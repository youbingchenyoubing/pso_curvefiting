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
reload(sys);
sys.setdefaultencoding("utf8")
weight=[]
print('CPCR Curve fitting')
print('  the function is a+b*x+c/((1+math.exp(-d*(x-e)))*(1+math.exp(-f*(x-g))))')
print('  the program use pso to optimze the parameter of fuction above')
length=0
def RMSE(parameters,*args):
    return RMSEWeight(parameters,args,0,length,weight) 
#caculate average of all number to shutdown the number 
def main():
    global weight
    global length
    weightfile=sys.argv[2]
    weight=readweightfile(weightfile) #if data have weight
    filename=sys.argv[1]
    function=sys.argv[3]
    data=readfile(filename)
    row,col=data.shape
    #print max(data[row-4])
    newbigger=[]
    for rownum in xrange(row):
         newbigger.append(data[rownum][col-1])
    midnum=caculatemidnum(newbigger)
    data=data/midnum
    if row>0:
        file_result=open('./result/result_weight.txt','w')
        file_result.write(repr('para_a').rjust(40)+repr('para_b').rjust(40)+repr('para_c').rjust(40)+repr('para_d').rjust(40)+repr('para_e').rjust(40)+repr('para_f').rjust(40)+repr('para_g').rjust(40)+repr('error').rjust(40)+'\n')
    for rownum in xrange(row):
        '''print data[rownum].min()
        print data[rownum].max()
        print data[rownum].mean()'''
        args=data[rownum]
        length=len(args)
        iteration=constraint(args,0,length-1)
        print('iterations={}'.format(iteration))
        minNum=args.min()
        maxNum=args.max()
        meanNum=args.mean()
        general=meanNum+maxNum
        radio=getArrange(args,length)/10
        #arrange=getArrangea(args,length)
        radiomax=radio*60
        radiomean=radio*meanNum
        lb=[-2,0,minNum,-1,-meanNum,-1,-meanNum]
        ub=[1,0.5,general+radiomean-maxNum,1.1,general+radiomax,1.1,general+radiomax]
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
        file_result.write(repr(xopt4[0]).rjust(40)+repr(xopt4[1]).rjust(40)+repr(xopt4[2]).rjust(40)+repr(xopt4[3]).rjust(40)+repr(xopt4[4]).rjust(40)+repr(xopt4[5]).rjust(40)+repr(xopt4[6]).rjust(40)+repr(fopt4).rjust(40)+'\n')
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
        print('please go to dir of result to save result_all.txt file\n')
if __name__=="__main__":
    main()


