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
        iteration=constraint(args,0,length-1)
        print('iterations={}'.format(iteration))
        minNum=args.min()
        maxNum=args.max()
        meanNum=args.mean()
        initialData=[minNum,numd,meanNum,0.1,maxNum,numf,maxNum]
        generalfit(initialData,0,length,method,args) 
    if row>0:
        print("***********************attention************************************")
        print('please go to dir of result to save result_general_itera.txt')
if __name__=="__main__":
    main()


    
