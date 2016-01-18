import numpy as np
import csv

arrange=30
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
    return maxposition-arrange


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
