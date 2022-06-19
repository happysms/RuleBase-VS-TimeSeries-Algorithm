from datetime import datetime

import numpy as np


def create_csv_using_only_model(result_df, model_name):
    """
    100일 통합 결과

    Args:
        result_df: df - 백테스트 완료 테이블
        model_name: arima

    Returns:
        csv 파일
    """
    df = result_df.copy()

    df["partition"] = ""
    df["partition"] = np.where((df["Datetime"] >= datetime(year=2021, month=5, day=10)) & (df["Datetime"] <= datetime(year=2021, month=7, day=21)), "loss1", df["partition"])
    df["partition"] = np.where((df["Datetime"] >= datetime(year=2021, month=11, day=18)) & (df["Datetime"] <= datetime(year=2022, month=2, day=6)), "loss2", df["partition"])
    df["partition"] = np.where((df["Datetime"] >= datetime(year=2019, month=2, day=17)) & (df["Datetime"] <= datetime(year=2019, month=7, day=15)), "profit1", df["partition"])
    df["partition"] = np.where((df["Datetime"] >= datetime(year=2020, month=10, day=8)) & (df["Datetime"] <= datetime(year=2021, month=4, day=17)), "profit2", df["partition"])

    condition = "ma"
    temp_df = backtest_ma(df)[["ror", "cr", "mdd", "rate"]]
    df[f"{condition}+return_of_rate"] = temp_df["ror"]
    df[f"{condition}+cumulative_return_of_rate"] = temp_df["cr"]
    df[f"{condition}+mdd"] = temp_df["mdd"]
    df[f"{condition}+rate"] = temp_df["rate"]

    condition = "rsi"
    temp_df = backtest_rsi(df)[["ror", "cr", "mdd", "rate"]]
    df[f"{condition}+return_of_rate"] = temp_df["ror"]
    df[f"{condition}+cumulative_return_of_rate"] = temp_df["cr"]
    df[f"{condition}+mdd"] = temp_df["mdd"]
    df[f"{condition}+rate"] = temp_df["rate"]

    condition = "noise"
    temp_df = backtest_noise(df)[["ror", "cr", "mdd", "rate"]]
    df[f"{condition}+return_of_rate"] = temp_df["ror"]
    df[f"{condition}+cumulative_return_of_rate"] = temp_df["cr"]
    df[f"{condition}+mdd"] = temp_df["mdd"]
    df[f"{condition}+rate"] = temp_df["rate"]

    condition = "ma_noise"
    temp_df = backtest_ma_and_noise(df)[["ror", "cr", "mdd", "rate"]]
    df[f"{condition}+return_of_rate"] = temp_df["ror"]
    df[f"{condition}+cumulative_return_of_rate"] = temp_df["cr"]
    df[f"{condition}+mdd"] = temp_df["mdd"]
    df[f"{condition}+rate"] = temp_df["rate"]

    condition = "ma_rsi"
    temp_df = backtest_ma_and_rsi(df)[["ror", "cr", "mdd", "rate"]]
    df[f"{condition}+return_of_rate"] = temp_df["ror"]
    df[f"{condition}+cumulative_return_of_rate"] = temp_df["cr"]
    df[f"{condition}+mdd"] = temp_df["mdd"]
    df[f"{condition}+rate"] = temp_df["rate"]

    condition = "rsi_noise"
    temp_df = backtest_noise_and_rsi(df)[["ror", "cr", "mdd", "rate"]]
    df[f"{condition}+return_of_rate"] = temp_df["ror"]
    df[f"{condition}+cumulative_return_of_rate"] = temp_df["cr"]
    df[f"{condition}+mdd"] = temp_df["mdd"]
    df[f"{condition}+rate"] = temp_df["rate"]

    condition = "ma_rsi_noise"
    temp_df = backtest_ma_and_rsi_and_noise(df)[["ror", "cr", "mdd", "rate"]]
    df[f"{condition}+return_of_rate"] = temp_df["ror"]
    df[f"{condition}+cumulative_return_of_rate"] = temp_df["cr"]
    df[f"{condition}+mdd"] = temp_df["mdd"]
    df[f"{condition}+rate"] = temp_df["rate"]

    df.rename(columns={"ror": "return of rate", "cr": "cumulative return of rate"}, inplace=True)
    file_name = f"only_{model_name}.csv"
    df.to_csv(file_name)

    return df

def create_csv_using_only_best_model(result_df, model_name, fitting_term):
    """
    최고 성능 모델

    Args:
        result_df: df - 백테스트 완료 테이블
        model_name: arima
        fitting_term: 100 - 학습 일 수

    Returns:
        csv 파일
    """
    df = result_df.copy()
    df["partition"] = ""
    df["partition"] = np.where((df["Datetime"] >= datetime(year=2021, month=5, day=10)) & (df["Datetime"] <= datetime(year=2021, month=7, day=21)), "loss1", df["partition"])
    df["partition"] = np.where((df["Datetime"] >= datetime(year=2021, month=11, day=18)) & (df["Datetime"] <= datetime(year=2022, month=2, day=6)), "loss2", df["partition"])
    df["partition"] = np.where((df["Datetime"] >= datetime(year=2019, month=2, day=17)) & (df["Datetime"] <= datetime(year=2019, month=7, day=15)), "profit1", df["partition"])
    df["partition"] = np.where((df["Datetime"] >= datetime(year=2020, month=10, day=8)) & (df["Datetime"] <= datetime(year=2021, month=4, day=17)), "profit2", df["partition"])

    condition = "ma"
    temp_df = backtest_ma(df)[["ror", "cr", "mdd", "rate"]]
    df[f"{condition}+return_of_rate"] = temp_df["ror"]
    df[f"{condition}+cumulative_return_of_rate"] = temp_df["cr"]
    df[f"{condition}+mdd"] = temp_df["mdd"]
    df[f"{condition}+rate"] = temp_df["rate"]

    condition = "rsi"
    temp_df = backtest_rsi(df)[["ror", "cr", "mdd", "rate"]]
    df[f"{condition}+return_of_rate"] = temp_df["ror"]
    df[f"{condition}+cumulative_return_of_rate"] = temp_df["cr"]
    df[f"{condition}+mdd"] = temp_df["mdd"]
    df[f"{condition}+rate"] = temp_df["rate"]

    condition = "noise"
    temp_df = backtest_noise(df)[["ror", "cr", "mdd", "rate"]]
    df[f"{condition}+return_of_rate"] = temp_df["ror"]
    df[f"{condition}+cumulative_return_of_rate"] = temp_df["cr"]
    df[f"{condition}+mdd"] = temp_df["mdd"]
    df[f"{condition}+rate"] = temp_df["rate"]

    condition = "ma_noise"
    temp_df = backtest_ma_and_noise(df)[["ror", "cr", "mdd", "rate"]]
    df[f"{condition}+return_of_rate"] = temp_df["ror"]
    df[f"{condition}+cumulative_return_of_rate"] = temp_df["cr"]
    df[f"{condition}+mdd"] = temp_df["mdd"]
    df[f"{condition}+rate"] = temp_df["rate"]

    condition = "ma_rsi"
    temp_df = backtest_ma_and_rsi(df)[["ror", "cr", "mdd", "rate"]]
    df[f"{condition}+return_of_rate"] = temp_df["ror"]
    df[f"{condition}+cumulative_return_of_rate"] = temp_df["cr"]
    df[f"{condition}+mdd"] = temp_df["mdd"]
    df[f"{condition}+rate"] = temp_df["rate"]

    condition = "rsi_noise"
    temp_df = backtest_noise_and_rsi(df)[["ror", "cr", "mdd", "rate"]]
    df[f"{condition}+return_of_rate"] = temp_df["ror"]
    df[f"{condition}+cumulative_return_of_rate"] = temp_df["cr"]
    df[f"{condition}+mdd"] = temp_df["mdd"]
    df[f"{condition}+rate"] = temp_df["rate"]

    condition = "ma_rsi_noise"
    temp_df = backtest_ma_and_rsi_and_noise(df)[["ror", "cr", "mdd", "rate"]]
    df[f"{condition}+return_of_rate"] = temp_df["ror"]
    df[f"{condition}+cumulative_return_of_rate"] = temp_df["cr"]
    df[f"{condition}+mdd"] = temp_df["mdd"]
    df[f"{condition}+rate"] = temp_df["rate"]
    df.rename(columns={"ror": "return_of_rate", "cr": "cumulative_return_of_rate"}, inplace=True)

    file_name = f"only_best_{model_name}_{fitting_term}.csv"
    df.to_csv(file_name)
    return df


def get_extracted_df_from_total_df(test_df, condition_list=[], partition=None):
    """

    Args:
        test_df:
        condition_list: ["ma"], ["ma", "noise"], ["ma", "noise", "rsi"]
        partition: profit1, profit2, loss1, loss2

    Returns:
        df
    """
    condition = ""

    if len(condition_list) == 0:
        condition = ""

    elif len(condition_list) == 1:
        if "rsi" in condition_list:
            condition = "rsi"
        elif "ma" in condition_list:
            condition = "ma"
        elif "noise" in condition_list:
            condition = "noise"

    elif len(condition_list) == 2:
        if "rsi" in condition_list and "ma" in condition_list:
            condition = "ma_rsi"
        elif "rsi" in condition_list and "noise" in condition_list:
            condition = "rsi_noise"
        elif "noise" in condition_list and "ma" in condition_list:
            condition = "ma_noise"


    elif len(condition_list) == 3:
        condition = "ma_rsi_noise"


    if len(condition):
        columns = ["Datetime", "Close", "partition", "prediction_close", f"{condition}+return_of_rate", f"{condition}+cumulative_return_of_rate", f"{condition}+mdd", f"{condition}+rate" ]
    else:
        columns = ["Datetime", "Close", "partition", "prediction_close", "return_of_rate", "cumulative_return_of_rate", "mdd", "rate" ]

    df = test_df[columns]
    columns = list(map(lambda x:x.split("+")[-1], columns))
    df.columns = columns

    if partition == "profit1":
        df = df[df["partition"] == "profit1"]
    elif partition == "profit2":
        df = df[df["partition"] == "profit2"]
    elif partition == "loss1":
        df = df[df["partition"] == "loss1"]
    elif partition == "loss2":
        df = df[df["partition"] == "loss2"]

    df['cumulative_return_of_rate'] = df['return_of_rate'].cumprod()
    df['mdd'] = (df['cumulative_return_of_rate'].cummax() - df['cumulative_return_of_rate']) / df['cumulative_return_of_rate'].cummax() * 100

    return df


def backtest_ma(test_df):
    df = test_df.copy()
    df['ma5'] = df['Open'].rolling(window=5).mean()
    df['ma10'] = df['Open'].rolling(window=10).mean()
    df['ma20'] = df['Open'].rolling(window=20).mean()
    df['ma50'] = df['Open'].rolling(window=50).mean()
    df['ma100'] = df['Open'].rolling(window=100).mean()

    df['rate'] = 0
    df['rate'] = np.where(df['ma5'] < df['Open'], df['rate'] + 1, df['rate'])
    df['rate'] = np.where(df['ma10'] < df['Open'], df['rate'] + 1, df['rate'])
    df['rate'] = np.where(df['ma20'] < df['Open'], df['rate'] + 1, df['rate'])
    df['rate'] = np.where(df['ma50'] < df['Open'], df['rate'] + 1, df['rate'])
    df['rate'] = np.where(df['ma100'] < df['Open'], df['rate'] + 1, df['rate'])
    df['rate'] = df['rate'] / 5

    df['trade'] = np.where((df['Open'] < df['prediction_close']) & (df['rate'] > 0), 1, 0)
    df['ror'] = np.where(df['trade'] == 1, 1 + (df['Close'] / df['Open'] - 1) * df['rate'], 1)
    df['cr'] = df['ror'].cumprod()
    df['mdd'] = (df['cr'].cummax() - df['cr']) / df['cr'].cummax() * 100
    return df


def backtest_noise(test_df):
    noise_ma = 30
    df = test_df.copy()
    df['ma5'] = df['Open'].rolling(window=5).mean()
    df['ma10'] = df['Open'].rolling(window=10).mean()
    df['ma20'] = df['Open'].rolling(window=20).mean()
    df['ma50'] = df['Open'].rolling(window=50).mean()
    df['ma100'] = df['Open'].rolling(window=100).mean()

    df['noise'] = 1 - abs(df['Open'] - df['Close']) / ((df['High']) * (1.0000001) - df['Low'])
    df['noise'] = df['noise'].shift(1)
    df['noise_ma'] = df['noise'].rolling(window=noise_ma).mean()

    df['rate'] = 0
    df['rate'] = np.where(df['noise_ma'] < 0.3, df['rate'] + 1, df['rate'])
    df['rate'] = np.where(df['noise_ma'] < 0.4, df['rate'] + 1, df['rate'])
    df['rate'] = np.where(df['noise_ma'] < 0.5, df['rate'] + 1, df['rate'])
    df['rate'] = np.where(df['noise_ma'] < 0.6, df['rate'] + 1, df['rate'])
    df['rate'] = np.where(df['noise_ma'] < 0.7, df['rate'] + 1, df['rate'])
    df['rate'] = df['rate'] / 5

    df['trade'] = np.where((df['Open'] < df['prediction_close']) & (df['rate'] > 0), 1, 0)
    df['ror'] = np.where(df['trade'] == 1, 1 + (df['Close'] / df['Open'] - 1) * df['rate'], 1)
    df['cr'] = df['ror'].cumprod()
    df['mdd'] = (df['cr'].cummax() - df['cr']) / df['cr'].cummax() * 100
    return df


def backtest_rsi(test_df):
    df = test_df.copy()
    df['rate'] = 1
    df['up'] = np.where(df['Close'].diff(1) > 0, df['Close'].diff(1), 0)
    df['down'] = np.where(df['Close'].diff(1) < 0, df['Close'].diff(1) * (-1), 0)
    df['au'] = df['up'].rolling(window=14, min_periods=14).mean()
    df['ad'] = df['down'].rolling(window=14, min_periods=14).mean()
    df['rsi'] = df['au'].div(df['ad'] + df['au']) * 100
    df['rsi_shift_1'] = df['rsi'].shift(1) # 하루 전의 rsi
    df['trade'] = np.where((df['Open'] < df['prediction_close']) & (df['rsi_shift_1'] > 40), 1, 0)
    df['ror'] = np.where(df['trade'] == 1, df['Close'] / df['Open'], 1)
    df['cr'] = df['ror'].cumprod()
    df['mdd'] = (df['cr'].cummax() - df['cr']) / df['cr'].cummax() * 100
    return df


def backtest_ma_and_noise(test_df):
    noise_ma = 30
    df = test_df.copy()
    df['noise'] = 1 - abs(df['Open'] - df['Close']) / ((df['High']) * (1.0000001) - df['Low'])
    df['noise'] = df['noise'].shift(1)
    df['noise_ma'] = df['noise'].rolling(window=noise_ma).mean()

    df['ma5'] = df['Open'].rolling(window=5).mean()
    df['ma10'] = df['Open'].rolling(window=10).mean()
    df['ma20'] = df['Open'].rolling(window=20).mean()
    df['ma50'] = df['Open'].rolling(window=50).mean()
    df['ma100'] = df['Open'].rolling(window=100).mean()

    df['rate'] = 0
    df['rate'] = np.where(df['ma5'] < df['Open'], df['rate'] + 1, df['rate'])
    df['rate'] = np.where(df['ma10'] < df['Open'], df['rate'] + 1, df['rate'])
    df['rate'] = np.where(df['ma20'] < df['Open'], df['rate'] + 1, df['rate'])
    df['rate'] = np.where(df['ma50'] < df['Open'], df['rate'] + 1, df['rate'])
    df['rate'] = np.where(df['ma100'] < df['Open'], df['rate'] + 1, df['rate'])
    df['rate'] = np.where(df['noise_ma'] < 0.3, df['rate'] + 1, df['rate'])
    df['rate'] = np.where(df['noise_ma'] < 0.4, df['rate'] + 1, df['rate'])
    df['rate'] = np.where(df['noise_ma'] < 0.5, df['rate'] + 1, df['rate'])
    df['rate'] = np.where(df['noise_ma'] < 0.6, df['rate'] + 1, df['rate'])
    df['rate'] = np.where(df['noise_ma'] < 0.7, df['rate'] + 1, df['rate'])
    df['rate'] = df['rate'] / 10

    df['trade'] = np.where((df['Open'] < df['prediction_close']) & (df['rate'] > 0), 1, 0)
    df['ror'] = np.where(df['trade'] == 1, 1 + (df['Close'] / df['Open'] - 1) * df['rate'], 1)
    df['cr'] = df['ror'].cumprod()
    df['mdd'] = (df['cr'].cummax() - df['cr']) / df['cr'].cummax() * 100
    return df


def backtest_ma_and_rsi(test_df):
    df = test_df.copy()
    df['up'] = np.where(df['Close'].diff(1) > 0, df['Close'].diff(1), 0)
    df['down'] = np.where(df['Close'].diff(1) < 0, df['Close'].diff(1) * (-1), 0)
    df['au'] = df['up'].rolling(window=14, min_periods=14).mean()
    df['ad'] = df['down'].rolling(window=14, min_periods=14).mean()
    df['rsi'] = df['au'].div(df['ad'] + df['au']) * 100
    df['rsi_shift_1'] = df['rsi'].shift(1) # 하루 전의 rsi

    df['ma5'] = df['Open'].rolling(window=5).mean()
    df['ma10'] = df['Open'].rolling(window=10).mean()
    df['ma20'] = df['Open'].rolling(window=20).mean()
    df['ma50'] = df['Open'].rolling(window=50).mean()
    df['ma100'] = df['Open'].rolling(window=100).mean()

    df['rate'] = 0
    df['rate'] = np.where(df['ma5'] < df['Open'], df['rate'] + 1, df['rate'])
    df['rate'] = np.where(df['ma10'] < df['Open'], df['rate'] + 1, df['rate'])
    df['rate'] = np.where(df['ma20'] < df['Open'], df['rate'] + 1, df['rate'])
    df['rate'] = np.where(df['ma50'] < df['Open'], df['rate'] + 1, df['rate'])
    df['rate'] = np.where(df['ma100'] < df['Open'], df['rate'] + 1, df['rate'])
    df['rate'] = df['rate'] / 5

    df['trade'] = np.where((df['Open'] < df['prediction_close']) & (df['rate'] > 0) & (df['rsi_shift_1'] > 40), 1, 0)  # rsi가 40이상일 경우에만 거래 진행
    df['ror'] = np.where(df['trade'] == 1, 1 + (df['Close'] / df['Open'] - 1) * df['rate'], 1)
    df['cr'] = df['ror'].cumprod()
    df['mdd'] = (df['cr'].cummax() - df['cr']) / df['cr'].cummax() * 100

    return df


def backtest_noise_and_rsi(test_df):
    df = test_df.copy()
    noise_ma = 30
    df['noise'] = 1 - abs(df['Open'] - df['Close']) / ((df['High']) * (1.0000001) - df['Low'])
    df['noise'] = df['noise'].shift(1)
    df['noise_ma'] = df['noise'].rolling(window=noise_ma).mean()
    df['up'] = np.where(df['Close'].diff(1) > 0, df['Close'].diff(1), 0)
    df['down'] = np.where(df['Close'].diff(1) < 0, df['Close'].diff(1) * (-1), 0)
    df['au'] = df['up'].rolling(window=14, min_periods=14).mean()
    df['ad'] = df['down'].rolling(window=14, min_periods=14).mean()
    df['rsi'] = df['au'].div(df['ad'] + df['au']) * 100
    df['rsi_shift_1'] = df['rsi'].shift(1) # 하루 전의 rsi

    df['rate'] = 0
    df['rate'] = np.where(df['noise_ma'] < 0.3, df['rate'] + 1, df['rate'])
    df['rate'] = np.where(df['noise_ma'] < 0.4, df['rate'] + 1, df['rate'])
    df['rate'] = np.where(df['noise_ma'] < 0.5, df['rate'] + 1, df['rate'])
    df['rate'] = np.where(df['noise_ma'] < 0.6, df['rate'] + 1, df['rate'])
    df['rate'] = np.where(df['noise_ma'] < 0.7, df['rate'] + 1, df['rate'])
    df['rate'] = df['rate'] / 5

    df['trade'] = np.where((df['Open'] < df['prediction_close']) & (df['rate'] > 0) & (df['rsi_shift_1'] > 40), 1, 0)  # rsi가 40이상일 경우에만 거래 진행
    df['ror'] = np.where(df['trade'] == 1, 1 + (df['Close'] / df['Open'] - 1) * df['rate'], 1)
    df['cr'] = df['ror'].cumprod()
    df['mdd'] = (df['cr'].cummax() - df['cr']) / df['cr'].cummax() * 100

    return df


def backtest_ma_and_rsi_and_noise(test_df):
    noise_ma = 30
    df = test_df.copy()
    df['up'] = np.where(df['Close'].diff(1) > 0, df['Close'].diff(1), 0)
    df['down'] = np.where(df['Close'].diff(1) < 0, df['Close'].diff(1) * (-1), 0)
    df['au'] = df['up'].rolling(window=14, min_periods=14).mean()
    df['ad'] = df['down'].rolling(window=14, min_periods=14).mean()
    df['rsi'] = df['au'].div(df['ad'] + df['au']) * 100
    df['rsi_shift_1'] = df['rsi'].shift(1) # 하루 전의 rsi

    df['noise'] = 1 - abs(df['Open'] - df['Close']) / ((df['High']) * (1.0000001) - df['Low'])
    df['noise'] = df['noise'].shift(1)
    df['noise_ma'] = df['noise'].rolling(window=noise_ma).mean()
    df['ma5'] = df['Open'].rolling(window=5).mean()
    df['ma10'] = df['Open'].rolling(window=10).mean()
    df['ma20'] = df['Open'].rolling(window=20).mean()
    df['ma50'] = df['Open'].rolling(window=50).mean()
    df['ma100'] = df['Open'].rolling(window=100).mean()

    df['rate'] = 0
    df['rate'] = np.where(df['ma5'] < df['Open'], df['rate'] + 1, df['rate'])
    df['rate'] = np.where(df['ma10'] < df['Open'], df['rate'] + 1, df['rate'])
    df['rate'] = np.where(df['ma20'] < df['Open'], df['rate'] + 1, df['rate'])
    df['rate'] = np.where(df['ma50'] < df['Open'], df['rate'] + 1, df['rate'])
    df['rate'] = np.where(df['ma100'] < df['Open'], df['rate'] + 1, df['rate'])
    df['rate'] = np.where(df['noise_ma'] < 0.3, df['rate'] + 1, df['rate'])
    df['rate'] = np.where(df['noise_ma'] < 0.4, df['rate'] + 1, df['rate'])
    df['rate'] = np.where(df['noise_ma'] < 0.5, df['rate'] + 1, df['rate'])
    df['rate'] = np.where(df['noise_ma'] < 0.6, df['rate'] + 1, df['rate'])
    df['rate'] = np.where(df['noise_ma'] < 0.7, df['rate'] + 1, df['rate'])
    df['rate'] = df['rate'] / 10

    df['trade'] = np.where((df['Open'] < df['prediction_close']) & (df['rate'] > 0) & (df['rsi_shift_1'] > 40), 1, 0)  # rsi가 40이상일 경우에만 거래 진행
    df['ror'] = np.where(df['trade'] == 1, 1 + (df['Close'] / df['Open'] - 1) * df['rate'], 1)
    df['cr'] = df['ror'].cumprod()
    df['mdd'] = (df['cr'].cummax() - df['cr']) / df['cr'].cummax() * 100

    return df


