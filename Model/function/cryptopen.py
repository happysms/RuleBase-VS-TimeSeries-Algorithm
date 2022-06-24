import pickle
import pandas as pd

def cryptopen(path):
    """ crypto pkl file open
    Args:
        path (string): 파일 경로
    """
    
    with open(path, "rb") as f:
        df = pickle.load(f)
    
    try:
        df.reset_index(inplace=True)
    except:
        df = df.drop('Datetime', axis=1)
        return df
    
    #df.reset_index(inplace=True)
    df.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
    df.set_index('Date', inplace=True)
    #df = df.drop('Datetime', axis=1)
    return df