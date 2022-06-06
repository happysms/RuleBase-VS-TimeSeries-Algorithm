from bot.algorithm import TimeSeriesAlgorithm
from bot.object import OrderObject, ConfigObject
from datetime import datetime
import time
from bot.rule_base_condition import RuleBaseCondition


def main_loop(order_object, config_object):
    is_updated = False

    while True:
        try:
            now = datetime.now()
            if now.hour == 23 and now.minute == 59:
                if not is_updated:
                    is_updated = True
                    df = order_object.get_candles_df()
                    current_price = df['close'][-1]
                    predicted_close = TimeSeriesAlgorithm.predict_close_price(df=df,
                                                                              algorithm=config_object.algorithm,
                                                                              feature=config_object.feature)

                    if predicted_close > current_price:
                        if order_object.position:
                            continue
                        else:
                            rate = RuleBaseCondition.get_trading_rate_from_rule_base_condition(df=df, condition=config_object.condition)
                            amount = order_object.get_available_amount(current_price) * rate
                            order_id = order_object.open_order(amount)
                            record_dict = order_object.get_record_dict(order_id)
                            order_object.store_record(record_dict)

                    else:
                        if order_object.position:
                            order_id = order_object.close_order()
                            record_dict = order_object.get_record_dict(order_id)
                            order_object.store_record(record_dict)
                        else:
                            continue

            elif now.hour == 0 and now.minute == 0:
                is_updated = False
                time.sleep(30)
            else:
                time.sleep(30)

        except Exception as e:
            print(e)


if "__main__" == __name__:
    order_object = OrderObject()
    config_object = ConfigObject()
    main_loop(order_object, config_object)
