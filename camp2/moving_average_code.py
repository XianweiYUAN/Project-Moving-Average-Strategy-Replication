#%% 导入第三方库
import tushare as ts
import pandas as pd
import math
#%% 连接并初始化数据库
token = '2764d200bfbbbd89a811e8377813b9432aa6b6dc36703f5a07e40e25'
ts.set_token(token)
pro = ts.pro_api()
#%%
'''
1. Function Programming
2. Object-orieted Programming
'''
# 1 数据获取
def get_close(ticker,startdate,enddate):
    '''
    根据股票代码、起止时间获取股票价格数据，输出格式为Dataframe(带有close)
    '''
    df = pro.daily(ts_code=ticker,
                   start_date=startdate,
                   end_date=enddate)
    '''
    extracted data
    1. null 2. duplicate 3. oulier
    '''
    df = df.reindex().set_index('trade_date').sort_index()
    df_close = df[['open','close']]
    return df_close
#%%
# 2 指标计算
def ma(df,n):
    '''
    根据股票价格数据和周期参数，计算Moving Avearge，输出格式为Dataframe（带有close和MA）
    '''
    df['MA'+str(n)] = df['close'].rolling(n).mean()
    return df
#%%
# 3 回测分析
#%%
'''
ma5 ma10 ma20
(1) ma5 ? ma10
(2) ma5 ? ma20
(3) ma10 ? ma20
'''
#%%
def MA_strategy(d):
    #初始化列
    df['cash'] = 0 #拥有的现金总量
    df['shares'] = 0 #持有股数
    df['outstanding'] = 0 #持有股价值
    df['cash'].iloc[0]=1000000 #初始化现金
    for i in range(1,len(df)): 
        if df['cash'].iloc[i-1] != 0:#开仓信号
            if df['ma5'].iloc[i] > df['ma10'].iloc[i]:
                df['outstanding'].iloc[i] = df['cash'].iloc[i-1]
                df['cash'].iloc[i]=0
                df['shares'].iloc[i] = df['outstanding'].iloc[i]/df['close'].iloc[i]
            else:#保持不开仓
                df['cash'].iloc[i] = df['cash'].iloc[i-1]
        else:
            if df['ma5'].iloc[i]<df['ma10'].iloc[i]:#平仓信号
                df['cash'].iloc[i] = df['shares'].iloc[i-1]*df['close'].iloc[i]
                df['outstanding'].iloc[i] = 0
                df['shares'].iloc[i] = 0
            else:#更新持仓信息
                df['shares'].iloc[i] = df['shares'].iloc[i-1]
                df['outstanding'].iloc[i] = df['shares'].iloc[i]*df['close'].iloc[i]
    df['total_capital'] = df['cash'] + df['outstanding']#总资产
    return df
#%%
# 4 策略表现
def performance(df):
    '''
    根据策略资金变化计算其年化收益、年化波动及夏普比率
    '''
    ret = df['money'][-1]/df['money'][0]-1
    ann_ret = pow(ret , 250/len(df)) - 1
    
    df['return'] = df['money'].pct_change()
    ann_vol = df['return'].std() * math.sqrt(250)
    
    sr = ann_ret / ann_vol
    return sr
#%%
# 5 参数优化
'''
s: [3,4,5]
l: [8,9,10,11,12]
'''
def optimize(short,long,df):
    '''
    根据不同周期组合的参数计算最优夏普比
    '''
    outcome = strategy_new(df,100,short,long)
    sr = performance(outcome)
    return sr
#%%
sr_list = []
for short in [3,4,5]:
    for long in [8,9,10,11,12]:
        sr_list.append(optimize(short,long,gzmt))
#%%
# Homework
# 1. 上述逻辑自己实现
# 2. 测试，短周期参数【3,6】，长周期参数【8,12】，共20组参数。设计上述参数优化函数，找到最佳夏普比的参数对。
# *3. 根据研究报告内容，尝试计算另外不同的指标（任选）完成上述测试过程。
#%%
# 提高策略收益的办法
'''
1、选择不同行业，历史表现较佳的股票。例如，贵州茅台、宁德时代、中信证券、美的集团、立讯精密。（等权分配资金）
2、指标细化及仓位管理：例如MA5、MA10、MA20，根据不等式成立的个数，调整仓位：(多头排列、空头排列)
   a. MA5 > MA10 > MA20，满仓买入；
   b. MA5 > MA20 > MA10，买入2/3仓位。
   c. MA20 > MA5 > MA10，买入1/3仓位。
   d. MA20 > MA10 > MA5，空仓。
3、多指标复合，结合不同技术指标（同时考虑满足情况）交易。
   a. 等权打分法；
   b. 基于历史表现，线性回归组合法；
   c. 非线性模型。
4、结合基本面：
   a. 动态跟踪企业财务、股价表现，动态调整优化选股池。（经营数据、盈利数据、成本费用、估值）
   b. 多因子模型（结合基本面及股票量价数据） --- MFM Model --- CAPM Model
'''        
#%%
# 学习路线       
'''
1、编程：C++、Python(R&MATLAB)、SQL类数据库
    a. 基础语法、函数方法、面向对象方法(OOP)；--- 基础
    b. Python Package: Pandas、Numpy、Scipy、Sk-learn、Keras;
    c. Project（Kaggle---数据分析、公众号）、Github（观察学习完整的代码逻辑）、Git--- 实战
    *d. 数据结构与算法（Leetcode）;
    **e. Linux系统、Unix系统、OS；
2、金融:
    a. 资讯：Wind、东方财富网；--- 基于观察到的信息去二次搜索
    b. 会计财务、估值（绝对估值法、相对估值法）；
    c. 交易品种：股票、债券、期货、期权；
    d. 各类策略：主观、量化、投资类策略、交易类策略；（报告）
3、数学：
    a. 时间序列：ARIMA、GARCH；
    b. 模型类：线性回归、机器学习、深度学习...； 
    c. 概率：概率论、随机微积分（期权）；
4、考证
    从业资格证、CFA、FRM、CPA、*CQF....
MentorAndy
'''        
  