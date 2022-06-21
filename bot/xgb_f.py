import requests
from datetime import datetime
import FinanceDataReader as fdr
import pandas as pd
from datetime import datetime


def Merge_FnG(input_df,shift_val=0,aver_val=0):
    url = ' https://api.alternative.me/fng/?limit=0'
    data = requests.get(url).json()
    value = []
    time = []
    for i in data['data']:
        value.append(i['value'])
        time.append(datetime.fromtimestamp(int(i['timestamp'])).strftime('%Y-%m-%d'))
    value = value[::-1]
    time = pd.to_datetime(time[::-1])
    fng = pd.Series(value,time,name='fng')
    fear_df=pd.DataFrame(fng)
    fear_df.reset_index(inplace=True)
    fear_df.columns = ['Date', 'fng_index']
    fear_df['fng_index']=pd.to_numeric(fear_df['fng_index'])
    ori_len=len(input_df)
    input_df=pd.merge(input_df,fear_df,how='outer',on='Date')
    input_df['fng_index']=input_df['fng_index'].fillna(44)
    input_df=input_df[:ori_len]
    
    if (shift_val !=0):
        input_df[f'fng_index_{shift_val}']=input_df['fng_index'].shift(shift_val)
        
    if (aver_val !=0):
        input_df[f'fng_index_{aver_val}mean']=input_df['fng_index'].rolling(window=aver_val).mean()

    
    input_df=input_df.fillna(method='bfill')
    
    return input_df

def Merge_NT(input_df,shift_val=0,aver_val=0):
    naver_trend_df=pd.read_csv("../naver_trend.csv")
    naver_trend_df=naver_trend_df[6:]
    naver_trend_df=naver_trend_df.reset_index(drop=True)
    naver_trend_df.columns = ['Date', 'trend_index']
    naver_trend_df['Date'] = pd.to_datetime(naver_trend_df['Date'], format="%Y-%m-%d")
    naver_trend_df['trend_index']=pd.to_numeric(naver_trend_df['trend_index'])
    input_df=pd.merge(input_df,naver_trend_df,on='Date')
    
    if (shift_val !=0):
        input_df[f'trend_index_{shift_val}']=input_df['trend_index'].shift(shift_val)
        
    if (aver_val !=0):
        input_df[f'trend_index_{aver_val}mean']=input_df['trend_index'].rolling(window=aver_val).mean()
    
    input_df=input_df.fillna(method='ffill')
        
    return input_df

def Merge_pandas_ta(input_df):
    adx = input_df.ta.adx()
    macd = input_df.ta.macd(fast=14, slow=24)
    rsi = input_df.ta.rsi()
    df = pd.concat([input_df, adx, macd, rsi], axis=1)
    #결측치 처리
    predict_df = df
    predict_df2 = predict_df.dropna(axis=1, how='all')
    predict_df3 = predict_df2.interpolate(method='values')
    predict_df4 = predict_df3.dropna(axis=0, how='any')
    predict_df5 = predict_df4.drop(['High', 'Low'], axis=1)
    input_df=predict_df5
    return input_df

def Merge_DJI(input_df):
    start_date = str(input_df['Date'].iloc[0])
    end_date = str(input_df['Date'].iloc[-1])
    DJI_df = fdr.DataReader('dji', start_date, end_date).reset_index()
    dji_df=DJI_df.drop(['Open','High','Low','Change'],axis=1)
    dji_df.rename({'close':'dji_c','Volume':'dji_v'},axis=1,inplace=True)
    input_df=pd.merge(input_df,dji_df,how='outer',on='Date')
    
    return input_df

def Merge_ECR(input_df):
    start_date = str(input_df['Date'].iloc[0])
    end_date = str(input_df['Date'].iloc[-1])
    exr=fdr.DataReader('USD/KRW', start_date, end_date).reset_index()
    exr=exr.drop(['Open','High','Low','Change'],axis=1)
    exr.rename({'close':'exc_c'},axis=1,inplace=True)
    input_df=pd.merge(input_df,exr,how='outer',on='Date')
    input_df=input_df.fillna(method='ffill')
    input_df=input_df.fillna(method='bfill')
    
    return input_df

def Merge_HR(input_df):
    HR_3y_df=pd.read_csv("../hash-rate_3y.csv")
    HR_all_df=pd.read_csv("../hash-rate_alltime.csv")
    start_date=HR_3y_df['Timestamp'].iloc[0]
    inter_index=HR_all_df.index[HR_all_df['Timestamp']==start_date].tolist()[0]
    HR_df=HR_all_df[:inter_index]
    HR_df=pd.concat([HR_df,HR_3y_df])
    HR_df=pd.concat([HR_df,HR_3y_df])
    a=pd.date_range(start=str(input_df['Date'].iloc[0]),end=str(input_df['Date'].iloc[-1]))
    HR_ori_df=pd.DataFrame(a)
    HR_ori_df.rename({0:'Timestamp'},axis=1,inplace=True)
    
    for i in range(len(HR_ori_df['Timestamp'])):
        HR_df['Timestamp'] = pd.to_datetime(HR_df['Timestamp'], format="%Y-%m-%d")
    
    HR_ori_df=pd.merge(HR_ori_df,HR_df,how='outer',on='Timestamp')
    HR_ori_df=HR_ori_df.drop_duplicates()
    HR_ori_df
    
    HR_ori_df=HR_ori_df.drop_duplicates()
    HR_ori_df=HR_ori_df.fillna(method='ffill')
    HR_ori_df=HR_ori_df.fillna(method='bfill')
    HR_ori_df.rename({'Timestamp':'Date'},axis=1,inplace=True)

    input_df=pd.merge(input_df,HR_ori_df,on='Date')
    
    return input_df

def preprocessing(input_df, len_lag) :
    # 이동평균선 추가 5,10,20
    moving_avg=[5,10,20]
    for i in moving_avg:
        input_df[f'{i}_close']=-1
    for index in range(len(input_df)):
        for i in moving_avg:
            input_df[f'{i}_close']=input_df['close'].rolling(window=i).mean()
        
    # p_lag:과거 가격, q_lag:과거 거래량 추가, pq_lag:거래대금 
    for lag in range(1,len_lag+1):
        input_df[f'p_lag_{lag}'] = -1
        input_df[f'q_lag_{lag}'] = -1 
        input_df[f'pq_lag_{lag}'] = -1
        for index in range(lag, len(input_df)):
            input_df.loc[index, f'p_lag_{lag}'] = input_df['close'][index-lag] #1일전, 2일전, ... 가격을 feature로 추가
            input_df.loc[index, f'q_lag_{lag}'] = input_df['volume'][index-lag] #1일전, 2일전, ... 거래량을 feature로 추가
            input_df.loc[index, f'pq_lag_{lag}'] = (input_df['close'][index-lag]*input_df['volume'][index-lag]) #1일전, 2일전, ... 거래량을 feature로 추가
            
def OBV_preprocessing(input_df):
    # OBV 산출 및 데이터 프레임에 추가 
    OBV=[]
    OBV.append(0)
    for i in range(1,len(input_df)):
        if input_df['close'].iloc[i] > input_df['close'].iloc[i-1]:
            OBV.append(OBV[-1]+input_df['volume'].iloc[i])
        elif input_df['close'].iloc[i]<input_df['close'].iloc[i-1]:
            OBV.append(OBV[-1]-input_df['volume'].iloc[i]) 
        else:
            OBV.append(OBV[-1])
            
    # OBV 추가
    input_df['obv']=OBV
    
    # 지수 평균 이동값 계산 
    input_df['obv_ema']=input_df['obv'].ewm(com=20).mean()
    
    # obv가 보통 지수를 위로 뚫으면 매수 신호 아래로 뚫으면 매도 신호 
    input_df['signal_obv']=input_df['obv']-input_df['obv_ema']
    
    moving_avg=[5,20,30]
    for i in moving_avg:
        input_df[f'obv_lag{i}']=-1
    for index in range(len(input_df)):
        for i in moving_avg:
            input_df[f'obv_lag{i}']=input_df['signal_obv'].rolling(window=i).mean()

def gen_train_test2(input_df):
    input_df['target']=0
    for i in range(len(input_df)-1):
        input_df['target'].iloc[i]=input_df['close'].iloc[i+1]
