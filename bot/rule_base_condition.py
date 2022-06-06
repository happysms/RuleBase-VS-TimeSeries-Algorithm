import numpy as np
from bot.object import OrderObject, ConfigObject


class RuleBaseCondition:
    @classmethod
    def get_trading_rate_from_rule_base_condition(cls, df, condition):
        if len(condition) == 0:
            return 1

        if len(condition) == 1:
            if "ma" in condition:
                return cls.check_ma(df)

            elif "rsi" in condition:
                return cls.check_rsi(df)

            elif "noise" in condition:
                return cls.check_noise(df)

        elif len(condition) == 2:
            if "ma" in condition and "rsi" in condition:
                return cls.check_ma_and_rsi(df)
            elif "ma" in condition and "noise" in condition:
                return cls.check_ma_and_noise(df)
            elif "rsi" in condition and "noise" in condition:
                return cls.check_rsi_and_noise(df)

        elif len(condition) == 3:
            if "rsi" in condition and "noise" in condition and "ma" in condition:
                return cls.check_ma_and_noise_and_rsi(df)

        else:
            raise Exception()


    @staticmethod
    def check_ma(test_df):
        df = test_df.copy()
        ma5 = df['open'].rolling(window=5).mean()[-1]
        ma10 = df['open'].rolling(window=10).mean()[-1]
        ma20 = df['open'].rolling(window=20).mean()[-1]
        ma50 = df['open'].rolling(window=50).mean()[-1]
        ma100 = df['open'].rolling(window=100).mean()[-1]
        cur_price = df['close'].iloc[-1]
        rate = 0

        if ma5 < cur_price:
            rate += 1
        elif ma10 < cur_price:
            rate += 1
        elif ma20 < cur_price:
            rate += 1
        elif ma50 < cur_price:
            rate += 1
        elif ma100 < cur_price:
            rate += 1

        rate /= 5
        return rate

    @staticmethod
    def check_noise(test_df):
        noise_ma = 30
        df = test_df.copy()
        df['noise'] = 1 - abs(df['open'] - df['close']) / ((df['high']) * (1.0000001) - df['low'])
        df['noise'] = df['noise'].shift(1)
        noise = df['noise'].rolling(window=noise_ma).mean()[-1]
        rate = 0

        if noise < 0.3:
            rate += 1
        elif noise < 0.4:
            rate += 1
        elif noise < 0.5:
            rate += 1
        elif noise < 0.6:
            rate += 1
        elif noise < 0.7:
            rate += 1

        rate /= 5

        return rate

    @staticmethod
    def check_rsi(test_df):
        df = test_df.copy()
        rate = 0
        df['up'] = np.where(df['close'].diff(1) > 0, df['close'].diff(1), 0)
        df['down'] = np.where(df['close'].diff(1) < 0, df['close'].diff(1) * (-1), 0)
        df['au'] = df['up'].rolling(window=14, min_periods=14).mean()
        df['ad'] = df['down'].rolling(window=14, min_periods=14).mean()
        df['rsi'] = df['au'].div(df['ad'] + df['au']) * 100
        df['rsi_shift_1'] = df['rsi'].shift(1)  # 하루 전의 rsi
        rsi = df['rsi_shift_1'].iloc[-1]

        if rsi > 40:
            rate = 1

        return rate

    @staticmethod
    def check_ma_and_rsi(test_df):
        df = test_df.copy()
        ma5 = df['open'].rolling(window=5).mean()[-1]
        ma10 = df['open'].rolling(window=10).mean()[-1]
        ma20 = df['open'].rolling(window=20).mean()[-1]
        ma50 = df['open'].rolling(window=50).mean()[-1]
        ma100 = df['open'].rolling(window=100).mean()[-1]
        cur_price = df['close'].iloc[-1]
        rate = 0

        if ma5 < cur_price:
            rate += 1
        elif ma10 < cur_price:
            rate += 1
        elif ma20 < cur_price:
            rate += 1
        elif ma50 < cur_price:
            rate += 1
        elif ma100 < cur_price:
            rate += 1

        rate /= 5

        df['up'] = np.where(df['close'].diff(1) > 0, df['close'].diff(1), 0)
        df['down'] = np.where(df['close'].diff(1) < 0, df['close'].diff(1) * (-1), 0)
        df['au'] = df['up'].rolling(window=14, min_periods=14).mean()
        df['ad'] = df['down'].rolling(window=14, min_periods=14).mean()
        df['rsi'] = df['au'].div(df['ad'] + df['au']) * 100
        df['rsi_shift_1'] = df['rsi'].shift(1)  # 하루 전의 rsi
        rsi = df['rsi_shift_1'].iloc[-1]

        if rsi < 40:
            rate = 0

        return rate

    @staticmethod
    def check_ma_and_noise(test_df):
        df = test_df.copy()
        ma5 = df['open'].rolling(window=5).mean()[-1]
        ma10 = df['open'].rolling(window=10).mean()[-1]
        ma20 = df['open'].rolling(window=20).mean()[-1]
        ma50 = df['open'].rolling(window=50).mean()[-1]
        ma100 = df['open'].rolling(window=100).mean()[-1]
        cur_price = df['close'].iloc[-1]
        rate = 0

        if ma5 < cur_price:
            rate += 1
        elif ma10 < cur_price:
            rate += 1
        elif ma20 < cur_price:
            rate += 1
        elif ma50 < cur_price:
            rate += 1
        elif ma100 < cur_price:
            rate += 1

        df['noise'] = 1 - abs(df['open'] - df['close']) / ((df['high']) * (1.0000001) - df['low'])
        df['noise'] = df['noise'].shift(1)
        noise = df['noise'].rolling(window=30).mean()[-1]
        rate = 0

        if noise < 0.3:
            rate += 1
        elif noise < 0.4:
            rate += 1
        elif noise < 0.5:
            rate += 1
        elif noise < 0.6:
            rate += 1
        elif noise < 0.7:
            rate += 1

        rate /= 10
        return rate

    @staticmethod
    def check_rsi_and_noise(test_df):
        df = test_df.copy()
        rate = 0
        df['up'] = np.where(df['close'].diff(1) > 0, df['close'].diff(1), 0)
        df['down'] = np.where(df['close'].diff(1) < 0, df['close'].diff(1) * (-1), 0)
        df['au'] = df['up'].rolling(window=14, min_periods=14).mean()
        df['ad'] = df['down'].rolling(window=14, min_periods=14).mean()
        df['rsi'] = df['au'].div(df['ad'] + df['au']) * 100
        df['rsi_shift_1'] = df['rsi'].shift(1)  # 하루 전의 rsi
        rsi = df['rsi_shift_1'].iloc[-1]
        df['noise'] = 1 - abs(df['open'] - df['close']) / ((df['high']) * (1.0000001) - df['low'])
        df['noise'] = df['noise'].shift(1)
        noise = df['noise'].rolling(window=30).mean()[-1]

        if noise < 0.3:
            rate += 1
        elif noise < 0.4:
            rate += 1
        elif noise < 0.5:
            rate += 1
        elif noise < 0.6:
            rate += 1
        elif noise < 0.7:
            rate += 1

        rate /= 5
        if rsi < 40:
            rate = 0

        return rate

    @staticmethod
    def check_ma_and_noise_and_rsi(test_df):
        df = test_df.copy()
        df['up'] = np.where(df['close'].diff(1) > 0, df['close'].diff(1), 0)
        df['down'] = np.where(df['close'].diff(1) < 0, df['close'].diff(1) * (-1), 0)
        df['au'] = df['up'].rolling(window=14, min_periods=14).mean()
        df['ad'] = df['down'].rolling(window=14, min_periods=14).mean()
        df['rsi'] = df['au'].div(df['ad'] + df['au']) * 100
        df['rsi_shift_1'] = df['rsi'].shift(1)  # 하루 전의 rsi
        rsi = df['rsi_shift_1'].iloc[-1]
        df['noise'] = 1 - abs(df['open'] - df['close']) / ((df['high']) * (1.0000001) - df['low'])
        df['noise'] = df['noise'].shift(1)
        noise = df['noise'].rolling(window=30).mean()[-1]

        ma5 = df['open'].rolling(window=5).mean()[-1]
        ma10 = df['open'].rolling(window=10).mean()[-1]
        ma20 = df['open'].rolling(window=20).mean()[-1]
        ma50 = df['open'].rolling(window=50).mean()[-1]
        ma100 = df['open'].rolling(window=100).mean()[-1]
        cur_price = df['close'].iloc[-1]
        rate = 0

        if ma5 < cur_price:
            rate += 1
        elif ma10 < cur_price:
            rate += 1
        elif ma20 < cur_price:
            rate += 1
        elif ma50 < cur_price:
            rate += 1
        elif ma100 < cur_price:
            rate += 1

        if noise < 0.3:
            rate += 1
        elif noise < 0.4:
            rate += 1
        elif noise < 0.5:
            rate += 1
        elif noise < 0.6:
            rate += 1
        elif noise < 0.7:
            rate += 1

        rate /= 10
        if rsi < 40:
            rate = 0

        return rate


if "__main__" == __name__:
    order_object = OrderObject()
    config_object = ConfigObject()
    df = order_object.get_candles_df()
    print(RuleBaseCondition.check_ma(df))
    print(RuleBaseCondition.check_noise(df))
    print(RuleBaseCondition.check_rsi(df))
    print(RuleBaseCondition.check_ma_and_noise(df))
    print(RuleBaseCondition.check_ma_and_rsi(df))
    print(RuleBaseCondition.check_rsi_and_noise(df))
    print(RuleBaseCondition.check_ma_and_noise_and_rsi(df))
