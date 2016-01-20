import numpy as np
from decimal import Decimal
from pyswarm import pso
import matplotlib.pyplot as plt
import math
import csv
import sys
import measure
from measure import *
import iterations
from iterations import *
print('CPCR Curve fitting')
print('  the function is a+b*x+c/((1+math.exp(-d*(x-e)))*(1+math.exp(-f*(x-g))))')
print('  the program use pso to optimze the parameter of fuction above')

def main():

    Xmin=0
    Xmax=90
    filename=sys.argv[1]
    method=sys.argv[2]
    numd=float(sys.argv[3])
    numf=float(sys.argv[4])
    if numd>1.1 or numd<-1 or numf>1.1 or numf<-1:
        print('error input args 3 or args 4')
        exit(0)
    data=readfile(filename)
    row,col=data.shape
    #print max(data[row-4])
    newbigger=[]
    for rownum in xrange(row):
         newbigger.append(data[rownum][col-1])
    midnum=caculatemidnum(newbigger)
    data=data/midnum
    if row>0:
        file_result_itera=open('./result/result_general_itera.txt','w')
        file_result_itera.write('this fit curve with method is ')
        file_result_itera.write(method)
        file_result_itera.write('\n\n')
        file_result_itera.close()
    for rownum in xrange(row):
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
        iteration=constraint(args,0,length-1)
        print('iterations={}'.format(iteration))
        minNum=args.min()
        maxNum=args.max()
        meanNum=args.mean()
        newdata=[]
        for i in xrange(Xmin,Xmax):
            newdata.append(args[i])
        initialData=[minNum,0.01,meanNum,numd,maxNum,numf,maxNum]
        generalfit(initialData,Xmin,Xmax,method,newdata) 
    if row>0:
        print("***********************attention************************************")
        print('please go to dir of result to save result_general_itera.txt')
if __name__=="__main__":
    main()


    
