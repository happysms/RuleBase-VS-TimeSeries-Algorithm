from errors import NotFoundAlgorithm
from statsmodels.tsa.arima.model import ARIMA
from object import OrderObject, ConfigObject
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Conv1D, Lambda, Dropout
from tensorflow.keras.losses import Huber
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
import numpy as np

#for LR
from sklearn.linear_model import LinearRegression
import pandas_ta as ta
import pandas as pd

#for xgb
import xgboost
import requests
from xgboost import XGBRegressor
import xgb_f as Xf

class TimeSeriesAlgorithm:

    @classmethod
    def predict_close_price(cls, df, algorithm: str, feature: list):
        if algorithm == "lstm":
            return cls.predict_close_price_from_lstm(df, feature)

        elif algorithm == "xgboost":
            return cls.predict_close_price_from_xgboost(df, feature)

        elif algorithm == "arima":
            return cls.predict_close_price_from_arima(df, feature)

        elif algorithm == "lr":
            return cls.predict_close_price_from_lr(df, feature)
        else:
            raise NotFoundAlgorithm()

    @staticmethod
    def predict_close_price_from_lr(df, feature):
        """
            df는 200일 동안의 1일 데이터
            return: 당일 예측 종가
        """
        model = LinearRegression()
        
        # TA 지표 수집 후 합치기
        adx = df.ta.adx()
        macd = df.ta.macd(fast=14, slow=24)
        rsi = df.ta.rsi()
        df = pd.concat([df, adx, macd, rsi], axis=1)
        
        # 이동평균선에 대한 결측치 제거
        df = df.dropna(axis=1, how='all')
        df = df.interpolate(method='values')
        df = df.dropna(axis=0, how='any')
        
        # 길이 101인 데이터프레임 생성
        df = df[len(df) - 101:]
        
        # 학습데이터 분할
        x_train, y_train = df[:100].drop("close", axis=1), df[:100]["close"]
        
        model.fit(x_train, y_train) # 100일 데이터 학습
        
        x_test = df[100:101].drop("close", axis=1) # 예측해야 할 값 분리
        [close_price] = model.predict(x_test)
        
        #print("predict_close_price : ", close_price)
        #print("true_close_price : ", df[100:101]["close"][0])
        
        return close_price

    @staticmethod
    def predict_close_price_from_xgboost(df, feature):
        model = XGBRegressor()
        df['Date']=df.index
        test_df=df[:]
        test_df=Xf.Merge_FnG(test_df,30,30)
        test_df=Xf.Merge_DJI(test_df)
        test_df=Xf.Merge_ECR(test_df)
        test_df=Xf.Merge_HR(test_df)
        price_df=test_df[:]
        Xf.OBV_preprocessing(price_df)
        Xf.preprocessing(price_df,10)
        df=price_df[:]

        df = df[len(df) - 101:]
        df.drop('Date',axis=1,inplace=True)
        print(df)

        x_train, y_train = df[:100].drop("close", axis=1), df[:100]["close"]
        model.fit(x_train, y_train)
        x_test = df[100:101].drop("close", axis=1) 
        [close_price] = model.predict(x_test)

        return close_price

    @staticmethod
    def predict_close_price_from_arima(df, feature):
        df = df[100:]['close']   # 100은 피팅 기간
        model = ARIMA(df, order=(2, 1, 2))  # 최적 파라미터
        model_fit = model.fit()
        full_forecast = model_fit.forecast(steps=1)  # 예측 일 수
        close_price = full_forecast[-1]
        return close_price

    @staticmethod
    def predict_close_price_from_lstm(df, feature):
        df = df[100:]

        scaler_x = MinMaxScaler()  # MinMaxScaling
        df[['open', 'high', 'low', 'volume']] = scaler_x.fit_transform(df[['open', 'high', 'low', 'volume']])

        scaler_y = MinMaxScaler()  # 나중에 예측종가를 MinMaxScaling하기 전의 원래 값으로 변환하기 위해 따로 scaler_y를 만듬
        df['close'] = scaler_y.fit_transform(df['close'].values.reshape(-1, 1))

        # ========  LSTM 학습을 위한 데이터 생성 함수
        def seq2dataset(df, window, horizon):
            X = []
            Y = []

            x_val, y_val = df.drop('close', axis=1, inplace=False), df['close']
            x_val = x_val.to_numpy()
            y_val = y_val.to_numpy()

            for i in range(0, len(df) - (window + horizon) + 1, 5):
                x = x_val[i:(i + window)]
                y = y_val[i + window + horizon - 1]
                X.append(x)
                Y.append(y)
            return np.array(X), np.array(Y)

        # ======== LSTM 학습 데이터셋 생성
        # 윈도우 w와 수평선 h

        w = 10  # 윈도우는 이전 요소 몇 개를 볼 것인지
        h = 1  # 수평선은 얼마나 먼 미래를 예측할 것인지

        train, test = df[:99], df[100 - w:100]
        X_train, y_train = seq2dataset(train, w, h)

        X_test, y_test = test.drop('close', axis=1, inplace=False), test['close']
        X_test = X_test.to_numpy()
        y_test = y_test.to_numpy()

        X_test = X_test.reshape(1, w, 4)
        y_test = y_test.reshape(1, w, 1)

        # LSTM 모델 구축
        model = Sequential()
        model.add(LSTM(units=256, activation='tanh', input_shape=X_train[0].shape))
        model.add(Dropout(0.2))
        model.add(Dense(1))

        # Sequence 학습에 비교적 좋은 퍼포먼스를 내는 Huber()를 사용한다.
        loss = Huber()
        optimizer = Adam(0.0005)
        model.compile(loss=Huber(), optimizer=optimizer, metrics=['mse'])

        # earlystopping은 10번 epoch통안 val_loss 개선이 없다면 학습을 멈춘다.
        earlystopping = EarlyStopping(monitor='val_loss', patience=10)

        # model fitting
        model.fit(X_train, y_train, epochs=100, batch_size=16, validation_split=0.3, callbacks=[earlystopping], verbose=0)

        # 예측
        pred = model.predict(X_test)

        # MinMaxScaling 이전의 종가로 다시 스케일링
        rescaled_pred = scaler_y.inverse_transform(np.array(pred).reshape(-1, 1))

        close_price = rescaled_pred[0][0]
        return close_price


if "__main__" == __name__:
    order_object = OrderObject()
    config_object = ConfigObject()
    print(order_object)
    print(config_object)

    df = order_object.get_candles_df()
    print(df)
    predicted_close = TimeSeriesAlgorithm.predict_close_price(df, config_object.algorithm, config_object.feature)
    print(predicted_close)


