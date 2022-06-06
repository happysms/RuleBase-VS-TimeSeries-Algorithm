import json
import ccxt
from typing import List
import time
import pandas as pd


class OrderObject:
    def __init__(self):
        with open("config.json", 'r') as file:
            data = json.load(file)
        self.position = data.get("position")
        self.ticker = data.get("ticker")
        self.balance = data.get("balance")
        self.amount = data.get("amount")
        self.spot_future = data.get("spot_future")
        self.exchange_object = self.get_exchange_object(data["api_key"], data["api_secret"], data["exchange"], self.spot_future)

    def __str__(self):
        return f"position: {self.position}"\
               f"ticker: {self.ticker}" \
               f"balance: {self.balance}"\
               f"amount: {self.amount}" \
               f"spot_future: {self.spot_future}"

    def get_exchange_object(self, api_key, api_secret, exchange, spot_future):
        if "binance" == exchange:
            exchange = ccxt.binance(config={
                # 'apiKey': api_key,
                # 'secret': api_secret,
                # 'enableRateLimit': True,
                'options': {
                    'defaultType': spot_future
                }
            })

        elif "bybit" == exchange:
            exchange = ccxt.bybit(config={
                'apiKey': api_key,
                'secret': api_secret,
                'enableRateLimit': True,
                'options': {
                    'defaultType': spot_future
                }
            })

        return exchange

    def get_candles_df(self):
        """
        Gets last candle and current candle data

        Returns:
            DataFrame: ('open', 42777.79) ('high', 42787.27) ('low', 42774.49) ('close', 42774.49) ('volume', 77.15)
            DataFrame: ('open', 42774.48) ('high', 42800.0) ('low', 42771.69) ('close', 42800.0) ('volume', 58.647)
        """

        # BTC_USDT -> BTC/USDT

        data = self.exchange_object.fetch_ohlcv(
            symbol=self.ticker,
            timeframe="1d",
            since=None,
            limit=200
        )

        df = pd.DataFrame(
            data=data,
            columns=['datetime', 'open', 'high', 'low', 'close', 'volume']
        )

        df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
        df.set_index('datetime', inplace=True)
        return df

    def open_order(self, amount):
        order = self.exchange_object.create_market_buy_order(symbol=self.ticker, amount=amount)
        self.amount = amount
        order_id = None
        if self.exchange_object.name.lower() == "bybit":
            order_id = order['info']['order_id']
        elif self.exchange_object.name.lower() == "binance":
            order_id = order['info']['orderId']

        # TODO: amount fix
        return order_id

    def get_available_amount(self, price):
        amount = self.balance / price
        return amount

    def close_order(self):
        order = self.exchange_object.create_market_sell_order(symbol=self.ticker, amount=self.amount)

        order_id = None
        if self.exchange_object.name.lower() == "bybit":
            order_id = order['info']['order_id']
        elif self.exchange_object.name.lower() == "binance":
            order_id = order['info']['orderId']
        return order_id

    def get_record_dict(self, order_id):
        if self.spot_future == "spot":
            timeout_count = 0
            record = None
            while True:
                try:
                    record = self.exchange_object.fetch_order(order_id, self.ticker)
                    if record['remaining'] != 0:
                        time.sleep(1)
                        timeout_count += 1

                        if timeout_count == 10:
                            raise Exception(f"Order remaining not filled: remaining={record['remaining']}, order_id={order_id}")
                        continue
                    break

                except ccxt.OrderNotFound:
                    time.sleep(1)
                    timeout_count += 1

                    if timeout_count == 10:
                        raise Exception(f"Order remaining not filled: remaining={record['remaining']}, order_id={order_id}")
        else:
            timeout_count = 0
            record = None

            while True:
                try:
                    record = self.exchange_object.fetch_order(order_id, self.ticker)
                    break
                except ccxt.OrderNotFound:
                    time.sleep(1)
                    timeout_count += 1

                    if timeout_count == 10:
                        raise Exception(f"Failed to fetch order: {order_id}")

        return record

    def store_record(self, record):
        try:
            with open("record.json", 'r') as file:
                data = json.load(file)

            data['record'].append(record)
            with open("record.json", 'w', encoding='utf-8') as file:
                json.dump(data, file, indent="\t")

        except FileNotFoundError:
            with open('record.json', 'w') as file:
                data = {"record": []}
                json.dump(data, file)


class ConfigObject:
    def __init__(self):
        with open("config.json", 'r') as file:
            data = json.load(file)

        self.algorithm = data.get("algorithm")
        self.feature: List = data.get("feature")
        self.condition: List = data.get("condition")

    def __str__(self):
        return f"algorithm: {self.algorithm}"\
               f"feature: {self.feature}" \
               f"condition: {self.condition}"

