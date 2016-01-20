import numpy as np
import matplotlib.pyplot as plt
import math
import scipy
from lmfit import minimize, Parameters,Model

def myfitfunction(x,a,b,c,d,e,f,g):
    return a+b*x+c/((1+np.exp(-d*(x-e)))*(1+np.exp(-f*(x-g))))


def generalfit(vars,Xmin,Xmax,method,data):
    mymod=Model(myfitfunction)
    x=np.array(range(Xmin+1,Xmax+1),int)
    #params=getparams(vars)
    mymod.set_param_hint('a',value=vars[0])
    mymod.set_param_hint('b',value=vars[1],min=0,max=0.5)
    mymod.set_param_hint('c',value=vars[2])
    mymod.set_param_hint('d',value=vars[3],min=-1,max=1.1)
    mymod.set_param_hint('e',value=vars[4])
    mymod.set_param_hint('f',value=vars[5],min=-1,max=1.1)
    mymod.set_param_hint('g',value=vars[6])
    #print params
    '''newdata=[]
    for i in xrange(Xmin,Xmax):
        newdata.append(data[i])'''
    out=mymod.fit(data,x=x,method=method,jac=True)
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
    file_result=open('./result/result_general_itera.txt','r+')
    file_result.read()
    file_result.write(out.fit_report())
    file_result.write('\n\n')
    file_result.close()
    #file_result.write(out.params)
        
