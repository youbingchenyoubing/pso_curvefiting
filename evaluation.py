import numpy as np
import math
#give a x caculate y y=f(x)
def caculate(x,parameters):
    a,b,c,d,e,f,g=parameters
    return a+b*x+c/((1+np.exp(-d*(x-e)))*(1+np.exp(-f*(x-g))))
#caculate average of real data 
def caculatemean(args,Xmin,Xmax):
    size=0
    sum=0
    for i in xrange(Xmin,Xmax):
        sum=sum+args[i]
        size=size+1
    return sum/size
# the sum of square of residuals also called the residual sum of squares
def SSEfunction(parameters,args,Xmin,Xmax):
    y=args
    SSE=0
    for i in xrange(Xmin,Xmax):
        yi=caculate(i+1,parameters)
        SSE=SSE+math.pow((y[i]-yi),2) 
    return SSE
#proportional to the variance of the data
def SSTfunction(parameters,args,Xmin,Xmax):
    SST=0
    y=args
    meanvalue=caculatemean(args,Xmin,Xmax)
    for i in xrange(Xmin,Xmax):
        SST=SST+math.pow((y[i]-meanvalue),2)
    return SST

#coefficient of determination Rscore
def R_score(parameters,args,Xmin,Xmax):
    SSE=SSEfunction(parameters,args,Xmin,Xmax)
    SST=SSTfunction(parameters,args,Xmin,Xmax)
    return (SSE/SST)-1

#Adjusted Rscore
def Adjusted_R_score(parameters,args,Xmin,Xmax):
    size=Xmax-Xmin
    parametersize=len(parameters)
    Rscore=R_score(parameters,args,Xmin,Xmax)
    return (1+Rscore)*(parametersize/(size-parametersize-1))+Rscore

#MSE=SSE/n
def MSEfunction(parameters,args,Xmin,Xmax):
    SSE=SSEfunction(parameters,args,Xmin,Xmax)
    size=Xmax-Xmin
    return SSE/size
#RMSE=sqrt(MSE)
def RMSEfunction(parameters,args,Xmin,Xmax):
    MSE=MSEfunction(parameters,args,Xmin,Xmax)
    return math.sqrt(MSE)
#vote  mechanism RNSE and Rscore
def RMSEandRScore(parameters,args,Xmin,Xmax):
    return 0.5*RMSEfunction(parameters,args,Xmin,Xmax)+0.5*R_score(parameters,args,Xmin,Xmax)
