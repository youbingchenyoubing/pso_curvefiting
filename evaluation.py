import numpy as np
import matplotlib.pyplot as plt
import math
import scipy
from lmfit import minimize, Parameters,Model
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


# define RMSE with weight
def RMSEWeight(parameters,args,Xmin,Xmax,weight):
    size=0
    sum=0
    for i in xrange(Xmin,Xmax):
        size=size+1
        yi=caculate(i+1,parameters)
        sum=sum+math.pow(args[i]-yi,2)*weight[i]
    return math.sqrt(sum/size)
    
def residual(vars,x,data,eps_data):
    a,b,c,d,e,f,g=vars 
    model=a+b*x+c/((1+exp(-d*(x-e)))*1+exp(-f*(x-g)))
    return (data-model)/eps_data

'''def leastqfunction(vars,x,data,eps_data):
    out=leastq(residual,vars,args=(x,data,eps_data))
    return out'''
def  residualData(params,x,data,eps_data):
    a= params['a'].value
    b=params['b'].value
    c=params['c'].value
    d=params['d'].value
    e=params['e'].value
    f=params['f'].value
    g=params['g'].value
    model=a+b*x+c/((1+np.exp(-d*(x-e)))*(1+np.exp(-f*(x-g))))
    return (model-data)/eps_data

def getparams(vars):
    params=Parameters()
    params.add('a',value=vars[0])
    params.add('b',value=vars[1],min=0,max=0.5)
    params.add('c',value=vars[2])
    params.add('d',value=vars[3],min=-1,max=1.1)
    params.add('e',value=vars[4])
    params.add('f',value=vars[5],min=-1,max=1.1)
    params.add('g',value=vars[6])
    return params
def getresult(parameters):
    result=[]
    result.append(parameters['a'].value)
    result.append(parameters['b'].value) 
    result.append(parameters['c'].value)
    result.append(parameters['d'].value)
    result.append(parameters['e'].value)
    result.append(parameters['f'].value)
    result.append(parameters['g'].value)
    return result 
def minimizefunction(vars,low,high,data):
    mymod=Model(myfitfunction)
    newdata=[]
    x=np.array(range(low,high),int)
    for i in xrange(low,high):
        newdata.append(data[i])
    #params=getparams(vars)
    mymod.set_param_hint('a',value=vars[0])
    mymod.set_param_hint('b',value=vars[1],min=0,max=0.5)
    mymod.set_param_hint('c',value=vars[2])
    mymod.set_param_hint('d',value=vars[3],min=-1,max=1.1)
    mymod.set_param_hint('e',value=vars[4])
    mymod.set_param_hint('f',value=vars[5],min=-1,max=1.1)
    mymod.set_param_hint('g',value=vars[6])
    #print params
    out=mymod.fit(newdata,x=x)
    #result=getresult(out.params)
    print(out.fit_report())
    #x1=np.linspace(1,length,10000)
    plt.plot(x,newdata,'blue',linestyle='dashed',marker='.')
    plt.plot(x,out.init_fit,'y',linewidth=2)
    plt.plot(x,out.best_fit,'r',linewidth=2)
    plt.xlabel("circle(Time)")
    plt.ylabel("fluorescence")
    plt.legend()
    plt.show()
    file_result=open('./result/result_select_itera.txt','r+')
    file_result.read()
    file_result.write(out.fit_report())
    file_result.write('\n\n')
    file_result.close()
    #file_result.write(out.params)
def myfitfunction(x,a,b,c,d,e,f,g):
    return a+b*x+c/((1+np.exp(-d*(x-e)))*(1+np.exp(-f*(x-g))))
def fitfunction(vars,length,data,weight=None,method='leastsq'):
    mymod=Model(myfitfunction)
    x=np.array(range(1,length+1),int)
    #params=getparams(vars)
    mymod.set_param_hint('a',value=vars[0])
    mymod.set_param_hint('b',value=vars[1],min=0,max=0.5)
    mymod.set_param_hint('c',value=vars[2])
    mymod.set_param_hint('d',value=vars[3],min=-1,max=1.1)
    mymod.set_param_hint('e',value=vars[4])
    mymod.set_param_hint('f',value=vars[5],min=-1,max=1.1)
    mymod.set_param_hint('g',value=vars[6])
    #print params
    out=mymod.fit(data,x=x,weight=weight)
    #result=getresult(out.params)
    print(out.fit_report())
    #x1=np.linspace(1,length,10000)
    plt.plot(x,data,'blue',linestyle='dashed',marker='.')
    plt.plot(x,out.init_fit,'y',linewidth=2)
    plt.plot(x,out.best_fit,'r',linewidth=2)
    plt.xlabel("circle(Time)")
    plt.ylabel("fluorescence")
    plt.legend()
    plt.show()
    file_result=open('./result/result_all_itera.txt','r+')
    file_result.read()
    file_result.write(out.fit_report())
    file_result.write('\n\n')
    file_result.close()
    #file_result.write(out.params)
