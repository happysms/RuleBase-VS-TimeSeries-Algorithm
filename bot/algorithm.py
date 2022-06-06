from errors import NotFoundAlgorithm
from statsmodels.tsa.arima.model import ARIMA
from object import OrderObject, ConfigObject


class TimeSeriesAlgorithm:

    @classmethod
    def predict_close_price(cls, df, algorithm: str, feature: list):
        if algorithm == "LSTM":
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
    def predict_close_price_from_lstm(df, feature):
        """
            df는 200일 동안의 1일 데이터
            return: 당일 예측 종가
        """
        close_price = None
        return close_price

    @staticmethod
    def predict_close_price_from_xgboost(df, feature):
        close_price = None
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
    def predict_close_price_from_lr(df, feature):
        close_price = None
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


