import numpy as np
from collections import defaultdict
from time import sleep
from datetime import datetime

import pandas as pd

from volstreet.config import logger, token_exchange_dict, latency_logger
from volstreet.decorators import (
    retry_angel_api,
    classproperty,
    timeit,
    access_rate_handler,
)
from volstreet.angel_interface.active_session import ActiveSession
from volstreet.angel_interface.login import wait_for_login


class LiveFeeds:
    price_feed = None
    order_feed = None

    @classproperty
    def order_book(self) -> list:
        return list(self.order_feed.data_bank.values())

    @classmethod
    def order_feed_connected(cls):
        return cls.order_feed is not None and cls.order_feed.connected

    @classmethod
    def price_feed_connected(cls):
        return (
            cls.price_feed is not None
            and cls.price_feed.connected
            and not cls.price_feed.connection_stale
        )

    @classmethod
    @wait_for_login
    def start_feeds(cls):
        cls.start_price_feed()
        cls.start_order_feed()

    @classmethod
    def close_feeds(cls):
        try:
            if cls.price_feed is not None:
                cls.price_feed.close_connection()
            if cls.order_feed is not None:
                cls.order_feed.close_connection()
        except Exception as e:
            logger.error(f"Error while closing live feeds: {e}")

    @classmethod
    def start_price_feed(cls):
        from volstreet.trade_interface.price_feed import PriceFeed

        pf = PriceFeed()
        pf.run_in_background()
        while not pf.connected:
            logger.info("Waiting for price feed to connect...")
            sleep(2)
        pf.subscribe_indices()
        cls.price_feed = pf

    @classmethod
    def start_order_feed(cls):
        from volstreet.angel_interface.order_websocket import OrderWebsocket

        of = OrderWebsocket.from_active_session()
        of.run_in_background()
        cls.order_feed = of


@retry_angel_api(data_type=lambda x: x["data"]["fetched"])
@access_rate_handler(delay=1.5)
@timeit(logger=latency_logger)
def _fetch_quotes(tokens: list, mode: str = "FULL"):
    payload = defaultdict(list)
    for token in tokens:
        exchange = token_exchange_dict.get(token)
        if exchange:
            payload[exchange].append(token)
    payload = dict(payload)
    return ActiveSession.obj.market_data(mode, payload)


def fetch_quotes(tokens: list, mode: str = "FULL", structure: str = "list"):
    quote_data = _fetch_quotes(tokens, mode)

    if structure.lower() == "dict":
        return {entry["symbolToken"]: entry for entry in quote_data}
    elif structure.lower() == "list":
        return quote_data
    else:
        raise ValueError(f"Invalid structure '{structure}'.")


@retry_angel_api(data_type="ltp")
def _fetch_ltp(exchange_seg, symbol, token):
    price_data = ActiveSession.obj.ltpData(exchange_seg, symbol, token)
    return price_data


@timeit(logger=latency_logger)
def fetch_ltp(exchange_seg, symbol, token, field="ltp"):
    if LiveFeeds.price_feed_connected() and token in LiveFeeds.price_feed.data_bank:
        price = LiveFeeds.price_feed.data_bank[token][field]
    else:
        latency_logger.info(f"Fetching {token} price from API.")
        price = _fetch_ltp(exchange_seg, symbol, token)
    return price


@retry_angel_api(max_attempts=10)
@access_rate_handler(delay=1.5)
def _fetch_book(fetch_func):
    data = fetch_func()
    return data


@timeit(logger=latency_logger)
def fetch_book(book: str, from_api: bool = False) -> list:
    if book == "orderbook":
        if LiveFeeds.order_feed_connected() and not from_api:
            return LiveFeeds.order_book
        return _fetch_book(ActiveSession.obj.orderBook)
    elif book in {"positions", "position"}:
        return _fetch_book(ActiveSession.obj.position)
    else:
        raise ValueError(f"Invalid book type '{book}'.")


def lookup_and_return(
    book, field_to_lookup, value_to_lookup, field_to_return=None
) -> np.ndarray | dict:
    def filter_and_return(data: list):
        if not isinstance(field_to_lookup, (list, tuple, np.ndarray)):
            field_to_lookup_ = [field_to_lookup]
            value_to_lookup_ = [value_to_lookup]
        else:
            field_to_lookup_ = field_to_lookup
            value_to_lookup_ = value_to_lookup

        if field_to_return is None:  # Return the entire entry
            return np.array(
                [
                    entry
                    for entry in data
                    if all(
                        (
                            entry[field] == value
                            if not isinstance(value, (list, tuple, np.ndarray))
                            else entry[field] in value
                        )
                        for field, value in zip(field_to_lookup_, value_to_lookup_)
                    )
                    and all(entry[field] != "" for field in field_to_lookup_)
                ]
            )

        elif isinstance(
            field_to_return, (list, tuple, np.ndarray)
        ):  # multiple fields are requested
            bucket = []
            for entry in data:
                if all(
                    (
                        entry[field] == value
                        if not isinstance(value, (list, tuple, np.ndarray))
                        else entry[field] in value
                    )
                    for field, value in zip(field_to_lookup_, value_to_lookup_)
                ) and all(entry[field] != "" for field in field_to_lookup_):
                    bucket.append({field: entry[field] for field in field_to_return})
            if len(bucket) == 0:
                return np.array([])
            else:
                return np.array(bucket)
        else:  # Return a numpy array as only one field is requested
            # Check if 'orderid' is in field_to_lookup_
            if "orderid" in field_to_lookup_:
                sort_by_orderid = True
                orderid_index = field_to_lookup_.index("orderid")
            else:
                sort_by_orderid = False
                orderid_index = None

            bucket = [
                (entry["orderid"], entry[field_to_return])
                if sort_by_orderid
                else entry[field_to_return]
                for entry in data
                if all(
                    (
                        entry[field] == value
                        if not isinstance(value, (list, tuple, np.ndarray))
                        else entry[field] in value
                    )
                    for field, value in zip(field_to_lookup_, value_to_lookup_)
                )
                and all(entry[field] != "" for field in field_to_lookup_)
            ]

            if len(bucket) == 0:
                return np.array([])
            else:
                if sort_by_orderid:
                    # Create a dict mapping order ids to their index in value_to_lookup
                    orderid_to_index = {
                        value: index
                        for index, value in enumerate(value_to_lookup_[orderid_index])
                    }
                    # Sort the bucket based on the order of 'orderid' in value_to_lookup
                    bucket.sort(key=lambda x: orderid_to_index[x[0]])
                    # Return only the field_to_return values
                    return np.array([x[1] for x in bucket])
                else:
                    return np.array(bucket)

    if not (
        isinstance(field_to_lookup, (str, list, tuple, np.ndarray))
        and isinstance(value_to_lookup, (str, list, tuple, np.ndarray))
    ):
        raise ValueError(
            "Both 'field_to_lookup' and 'value_to_lookup' must be strings or lists."
        )

    if isinstance(field_to_lookup, list) and isinstance(value_to_lookup, str):
        raise ValueError(
            "Unsupported input: 'field_to_lookup' is a list and 'value_to_lookup' is a string."
        )

    if isinstance(book, list):
        return filter_and_return(book)
    elif isinstance(book, str) and book in {"orderbook", "positions"}:
        book_data = fetch_book(book)
        return filter_and_return(book_data)
    else:
        logger.error(f"Invalid book type '{book}'.")
        raise ValueError("Invalid book type.")


@retry_angel_api()
@access_rate_handler(delay=1.5)
def fetch_historical_prices(
    token: str, interval: str, from_date: datetime, to_date: datetime
):
    from_date = pd.to_datetime(from_date) if isinstance(from_date, str) else from_date
    to_date = pd.to_datetime(to_date) if isinstance(to_date, str) else to_date
    exchange = token_exchange_dict[token]
    historic_param = {
        "exchange": exchange,
        "symboltoken": token,
        "interval": interval,
        "fromdate": from_date.strftime("%Y-%m-%d %H:%M"),
        "todate": to_date.strftime("%Y-%m-%d %H:%M"),
    }
    return ActiveSession.obj.getCandleData(historic_param)
