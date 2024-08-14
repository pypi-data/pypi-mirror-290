# coding: utf-8

"""
    SnapTrade

    Connect brokerage accounts to your app for live positions and trading

    The version of the OpenAPI document: 1.0.0
    Contact: api@snaptrade.com
    Created by: https://snaptrade.com/
"""

from datetime import datetime, date
import typing
from enum import Enum
from typing_extensions import TypedDict, Literal, TYPE_CHECKING


class RequiredAmountNullable(TypedDict):
    pass

class OptionalAmountNullable(TypedDict, total=False):
    # Total value denominated in the currency of the `currency` field.
    amount: typing.Union[int, float]

    # The ISO-4217 currency code for the amount.
    currency: str

class AmountNullable(RequiredAmountNullable, OptionalAmountNullable):
    pass
