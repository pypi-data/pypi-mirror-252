from dataclasses import dataclass, asdict
from enum import Enum
from pandas.tseries import offsets
import datetime as dt
import pandas as pd
from uuid import uuid1
import numpy as np


class Action(Enum):
    BUY = 'BUY'
    SELL = 'SELL'


class OrderType(Enum):
    MKT = 'MKT'
    STP = 'STP'
    LMT = 'LMT'


@dataclass(slots=True)
class OCOEntries:
    orders = []
    oco_id = uuid1()

    def __init__(self, *args):
        for o in args:
            self.add(o)

    def add(self, other):
        if isinstance(other, Order):
            self.orders.append(other)
        else:
            raise TypeError('Not OrderDetails Object!')

    def __repr__(self):
        return f'OCOEntries({self.orders})'

    def as_dataframe(self):
        df = pd.DataFrame({'id': self.oco_id, 'orders': self.orders})
        df = df.explode('orders')
        df['orders'] = df.orders.apply(asdict)
        df_orders = pd.json_normalize(df.orders)
        df = pd.concat([df.drop('orders', axis=1), df_orders], axis=1)

        df['signal'] = df['action'].apply(lambda x: {'BUY': 1, 'SELL': -1}.get(x.value))
        df['pt_offset'] = df.profit_target_px
        df['sl_offset'] = df.stoploss_px
        df['bt_offset'] = df.breakeven_trigger_px
        df['entry_type'] = df.order_type
        df['entry_price'] = df.signal_px
        df['datetime'] = df.signal_time
        df['signal_timeout'] = df.signal_ttl
        return df


@dataclass(slots=True)
class Order:
    signal_time: (dt.datetime | pd.Timestamp)
    action: (Action | None)
    signal_px: (float | None)
    quantity: int = 1

    order_type: OrderType | None = OrderType.MKT
    signal_ttl: (offsets.DateOffset, dt.time, None) = pd.offsets.Minute(30)
    profit_target_px: float = np.nan
    stoploss_px: float = np.nan

    breakeven_trigger_px: float | bool = False
    breakeven_stoploss_px = float = np.nan

    closeout_ttl: (offsets.DateOffset, dt.time, None) = pd.NaT  # pd.offsets.Hour(1)

    def __repr__(self):
        return f'Order({self.action.value} {self.quantity} @ {self.signal_px} {self.order_type.value})'
