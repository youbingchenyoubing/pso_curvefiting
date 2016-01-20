# CCPCR 荧光曲线拟合



## 这个源代码依赖库包括
> numpy 1.10.4
> scipy  0.16.1
> matplotlib 1.1.1rc
> limfit

#### 本程序运行在Ubuntu12.04 平台上

********

##### 主要包含下面几个主要python脚本文件

* pso_all.py(读取 荧光数据文件csv,并且采用评价函数指标有SSE,RMSE,Rscore,ajustRscore等为粒子群的适应函数)
* ---
* pso_all_low.py （读取 荧光数据文件csv,并且采用评价函数指标有SSE,RMSE,Rscore,ajustRscore等为粒子群的适应函数）这两者不同在于粒子群优化参数范围不同，pso_all.py针对一般数据,pso_all_low.py在对在[1-60]之间起来的曲线拟合很不错,超过了pso_all.py对这部分曲线拟合的效果，但是在[60,90]之间数据起来的效果要大大超过pso_all.py拟合效果
* ---
* pso_all_high.py 相对前面两个的脚本而言,这个脚本只进行粒子群优化，没有经过一般的迭代拟合方法，上面两个脚本采用的是默认的Levenberg-Marquardt算法。
* ---
* pso_weight.py 是针对荧光实验数据的自定义权重大小。格式见./csvdata/weight.csv文件
* ---
* pso_select_2.py 是针对荧光实验数据关键点的拟合，对于关键点的选择详细见论文
* ---
* pso_select.py 是上面的脚本的粒子群算法拟合后再采用普通迭代的算法来进一步拟合（默认也是Levenberg-Marquardt算法）。
* ----
* compare_pso.py主要是用一般的算法比如（Levenberg-Marquardt算法,Newton-CG算法等）这些算法容易陷入局部最优，所以对于初始解的选取特别的重要
*----
* compare_pso_select.py 也是采用一般的算法来对关键曲线节点进行拟合
************
### usage
* python pso_all.py ./csvdata/file.csv RMSE(SSE,RScore,RMRS等)
* ----
* python pso_all_low.py ./csvdata/file.csv RMSE
* 
* python pso_all_high.py ./csvdata/file.csv RMSE
*----
* python pso_weight.py ./csvdata/file.csv ./csvdata/weight.csv RMSE
* ----
* python pso_select_2.py ./csvdata/file.csv RMSE
* ----
* python pso_select.py ./csvdata/file.csv RMSE
* ----
* python compare_pso.py ./csvdata/file.csv leastsq initial_data(这个我这边初始化两个，其他参数由程序生成) 
* ----
* python compare_pso_select.py ./csvdatat/<file>.csv leastsq <initial data>
*********************************
#### 其他
![Alt text](./image/1.png)
***********************************
**最后结果都存在./result/文件夹中**

