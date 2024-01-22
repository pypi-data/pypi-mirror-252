# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2024-01-22 14:06:05
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : SINA worm methods.
"""


from typing import List, Tuple, Dict, Union
from re import findall as re_findall
from reytool.rcomm import request
from reytool.rtime import now


__all__ = (
    "get_stock_info_table",
)


def get_stock_info_table(code: Union[str, List[str]]) -> List[Dict]:
    """
    Get stock information table.

    Parameters
    ----------
    code : Stock code.

    Returns
    -------
    Stock information table.
    """

    # Get parameter.
    if code.__class__ != str:
        code = ",".join(code)
    url = "https://hq.sinajs.cn/rn=%s&list=%s" % (
        now("timestamp"),
        code
    )
    headers = {"Referer": "https://finance.sina.com.cn"}

    # Request.
    response = request(
        url,
        headers=headers,
        check=True
    )

    # Extract.
    pattern = "([^_]+?)=\"([^\"]*)\""
    result: List[Tuple[str, str]] = re_findall(pattern, response.text)
    table = []
    for code, info in result:
        (
            stock_name,
            stock_open,
            stock_pre_close,
            stock_price,
            stock_high,
            stock_low,
            _,
            _,
            stock_volume,
            stock_amount,
            *_,
            stock_date,
            stock_time,
            _,
            _
        ) = info.split(",")
        row = {
            "code": code,
            "name": stock_name,
            "price": float(stock_price),
            "open": float(stock_open),
            "pre_close": float(stock_pre_close),
            "high": float(stock_high),
            "low": float(stock_low),
            "volume": int(stock_volume),
            "amount": int(stock_amount),
            "time": "%s %s" % (stock_date, stock_time),
        }
        row["change"] = round(row["price"] - row["pre_close"], 4)
        row["change_rate"] = round(row["change"] / row["pre_close"] * 100, 4)
        row["swing"] = round((row["high"] - row["low"]) / row["high"] * 100, 4)
        table.append(row)

    return table