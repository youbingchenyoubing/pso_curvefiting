import numpy as np
import csv

arrange=30
def getMinMax(length,maxPosition):
    Xmin=Xmax=0
    if maxPosition<20:
        Xmin=0
        Xmax=maxPosition+40-(maxPosition-Xmin)
    elif maxPosition>length-20:
        Xmax=length-1
        Xmin=maxPosition-40+(Xmax-maxPosition)
    else:
        Xmax=maxPosition+20
        Xmin=maxPosition-20
    return Xmin,Xmax
def parition(array,p,r):
    x=array[r]
    i=p-1
    for j in range(p,r):
        if (array[j]<x):
            i+=1
            array[j],array[i]=array[i],array[j]
    i+=1
    array[i],array[r]=array[r],array[i]
    return i
def quick_sort(array,p,r):
    if p<r:
        q=parition(array,p,r)
        quick_sort(array,p,q-1)
        quick_sort(array,q+1,r)
#dissication for
def getX(data,length):
    maxNum=0
    maxPositio=-1
    for i in xrange(1,length):
        if data[i]-data[i-1]>maxNum and data[i-1]>=0:
            maxNum=data[i]-data[i-1]
            maxPosition=i
    return maxPosition+1

#  
def getX_2(data,length):
    maxNum=0
    maxPosition=-1
    for i in xrange(1,length-1):
        if data[i-1]>0 and data[i]>0 and(data[i])/data[i-1]>maxNum:
            maxNum=(data[i])/data[i-1]
            maxPosition=i
    return maxPosition+1
def getArrangea(data,length):
    maxPosition=getX_2(data,length)
    sum=0
    size=0
    for i in xrange(maxPosition):
        sum=sum+data[i]
        size=size+1
    return sum/size
def getArrange(data,length):
    maxposition=getX(data,length)
    global arrange
    arrange=30
    if maxposition>arrange:
        return maxposition-arrange
    else: return maxposition


def constraint(data,Xmin,Xmax):
    sum=200
    for i in xrange(Xmin,Xmax):
        if data[i+1]<data[i]:
            sum=sum+10

    return sum
# read csv data in csv format
def readfile(filename):
    rows=[]
    with open(filename) as f:
        f_csv=csv.reader(f)
        headers=next(f_csv)
        for row in f_csv:
            if row:
                rows.append(row)
    return np.array(np.transpose(rows),dtype=float)
#read weight data in csv format
def readweightfile(filename):
    rows=[]
    weightrows=[]
    with open(filename) as f:
        f_csv=csv.reader(f)
        header=next(f_csv)
        sum=0.0
        for row in f_csv:
            if row:
                newrow=float(row[0])
                sum=sum+newrow
                rows.append(newrow)
    for iteranum in rows:
        weightrows.append(iteranum/sum)
    return weightrows 
#caculate average of all number to shutdown the number 
def caculatemidnum(data):
    sum=0.0
    length=len(data)
    for itera in data:
        sum=sum+(itera)
    return sum/(length*60)
