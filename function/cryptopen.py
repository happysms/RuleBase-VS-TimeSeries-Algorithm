import pickle
import pandas as pd

def cryptopen(path): # crypto pkl file open
    with open(path, "rb") as f:
        df = pickle.load(f)
    
    try: # 인덱스가 없는 파일
        df.reset_index(inplace=True)
        df.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
        df.set_index('Date', inplace=True)

    except:
        # 이미 존재할 경우
        df.drop('Datetime', axis=1)