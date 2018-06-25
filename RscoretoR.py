import numpy as np
import matplotlib.pyplot as plt
import measure
from measure import *
import os
import sys

def main():
    #plt.figure(1)
    #plt.xlabel("circle(Time)")
    #plt.ylabel("raw fluorescence")
    filename=sys.argv[1]
    #filename2=sys.argv[2]
    data=readfile_Rs(filename)
    result2 = []

    for one_data in data:
        result2.append(get_result_2(float(one_data)))
    #parameters=readfile(filename2)
    #row,col=data.shape
    #print max(data[row-4])
    #newbigger=[]
    #for rownum in xrange(row):
         #newbigger.append(data[rownum][col-1])

    print result2

def get_result_2(Rscore):
    print "Rscore = ",Rscore
    Rscore_1 = 1-Rscore
    print "1-Rscore= ",Rscore_1
    ad = float(89.0/82.0)
    print "ad= ",ad
    AdRscore = Rscore_1*ad 
    print "AdRscore", AdRscore
    result = 1-AdRscore
    print "Result = {0},Rscore={1}" .format(result,Rscore)
    return result
if __name__=="__main__":
    main()
    
        

