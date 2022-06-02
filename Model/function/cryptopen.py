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
        # 인덱스가 없는 파일
        print("=" * 60)
        print("인덱스가 존재하지 않습니다.")
        print("인덱스 및 칼럼명을 설정합니다.")
        print("=" * 60)
        df1 = df.reset_index(inplace=True)
        df1.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
        df1.set_index('Date', inplace=True)
        return df1

    except:
        # 이미 존재할 경우
        print("=" * 60)
        print("인덱스가 이미 존재합니다.")
        print("후방의 데이터타임을 삭제합니다.")
        print("=" * 60)
        df = df.drop('Datetime', axis=1)
        return df