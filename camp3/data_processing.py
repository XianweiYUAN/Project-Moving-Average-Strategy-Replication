#%%
# 累加函数
def get_sum():
    sum_ = 0
    a = int(input('please enter a number:'))
    for i in range(a+1):
        sum_ += i
    print(sum_)
#%%
# 阶乘递归算法
def fact(n):
    if n==1:
        return 1
    return n*fact(n-1)

#%%
#设置token
import tushare as ts
ts.set_token('1ac8eec9176c92199ad99e202e31044d50965f7aa7b0d7dc385d1693')
pro = ts.pro_api()
df = pro.daily(ts_code='000980.SZ', start_date='20180101', end_date='20220218')
#%%
#导入数据

#%%指标计算
def get_ma(df,n):
    df['ma'+str(n)] = df['close'].rolling(n).mean()
    return df
#%%
def MA_strategy(df):
    #初始化列
    df['cash'] = 0 #拥有的现金总量
    df['shares'] = 0 #持有股数
    df['outstanding'] = 0 #持有股价值
    df['cash'].iloc[0]=1000000 #初始化现金
    for i in range(1,len(df)): 
        if df['cash'].iloc[i-1] != 0:#开仓信号
            if df['ma5'].iloc[i]>df['ma10'].iloc[i]:
                df['outstanding'].iloc[i] = df['cash'].iloc[i-1]
                df['cash'].iloc[i]=0
                df['shares'].iloc[i] = df['outstanding'].iloc[i]/df['close'].iloc[i]
            else:#保持不开仓
                df['cash'].iloc[i] = df['cash'].iloc[i-1]
        else:
            if df['ma5'].iloc[i] < df['ma10'].iloc[i]:#平仓信号
                df['cash'].iloc[i] = df['shares'].iloc[i-1]*df['close'].iloc[i]
                df['outstanding'].iloc[i] = 0
                df['shares'].iloc[i] = 0
            else:#更新持仓信息
                df['shares'].iloc[i] = df['shares'].iloc[i-1]
                df['outstanding'].iloc[i] = df['shares'].iloc[i]*df['close'].iloc[i]
    df['total_capital'] = df['cash'] + df['outstanding']#总资产
    return df
#%%
gzmt = get_close('600519.SH',
                 '20150101',
                 '20201231')
get_ma(gzmt,5)
get_ma(gzmt,10)
gzmt = gzmt.dropna()
#%%
outcome = MA_strategy(gzmt)
#%%






    