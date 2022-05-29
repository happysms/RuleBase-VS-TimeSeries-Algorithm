from bot.errors import NotFoundAlgorithm
from statsmodels.tsa.arima.model import ARIMA


class TimeSeriesAlgorithm:
    def predict_close_price(self, df, algorithm: str):
        if algorithm == "LSTM":
            return self.predict_close_price_from_lstm(df)

        elif algorithm == "xgboost":
            return self.predict_close_price_from_xgboost(df)

        elif algorithm == "arima":
            return self.predict_close_price_from_arima(df)

        elif algorithm == "lr":
            return self.predict_close_price_from_lr(df)

        else:
            raise NotFoundAlgorithm()

    def predict_close_price_from_lstm(self, df):
        """
            df는 200일 동안의 1일 데이터
            return: 당일 예측 종가
        """
        close_price = None
        return close_price

    def predict_close_price_from_xgboost(self, df):
        close_price = None
        return close_price

    def predict_close_price_from_arima(self, df):
        df = df[100:]['Close']   # 100은 피팅 기간
        model = ARIMA(df, order=(2, 1, 2))
        model_fit = model.fit()
        full_forecast = model_fit.forecast(steps=1)  # 예측 일 수
        close_price = full_forecast[-1]
        return close_price

    def predict_close_price_from_lr(self, df):
        close_price = None
        return close_price





