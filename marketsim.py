import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkstudy.EventProfiler as ep
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import copy
import math
import csv
import sys
import re


def get_timestamps(begin, end, symbols, time=16):
    """
    Creates the timestamps for begin to end with provided
    stock symbols.
    """
    #Offset because we need the last day to see it's final price.
    offset = dt.timedelta(days=1)
    begin = dt.datetime(begin[0], begin[1], begin[2])
    end = dt.datetime(end[0], end[1], end[2])
    dt_timeofday = dt.timedelta(hours=time)
    ldt_timestamps = du.getNYSEdays(begin, end + offset, dt_timeofday)
    return ldt_timestamps

def get_data(timestamps, symbols, keys, provider="Yahoo"):
    dataobj = da.DataAccess('Yahoo')
    data = dataobj.get_data(timestamps, symbols, keys)
    return dict(zip(keys, data))

def get_daily_returns(returns):
    na_rets = returns.copy()
    tsu.returnize0(na_rets)
    return na_rets


def get_cumulative_daily_returns(returns):
    x, y = returns.shape[0], returns.shape[1]
    cdr = np.ones((x, y))
    for row in range(1, x):
        cdr[row,:] = cdr[row - 1,:] * (1 + returns[row,:])
    return cdr[x - 1]


def parse_orders(filename):
    fileopen = open(filename, 'rU')
    parser = csv.reader(fileopen, delimiter=",")
    orders = {
        "year": [], "month": [], "date": [], "symbol": [], "buy_or_sell": [],
                    "quantity": []}
    for row in parser:
        orders["year"].append(row[0])
        orders["month"].append(row[1])
        orders["date"].append(row[2])
        orders["symbol"].append(row[3])
        orders["buy_or_sell"].append(row[4])
        orders["quantity"].append(row[5])
    begindate = [orders["year"][0], orders["month"][0], orders["date"][0]]
    enddate = [orders["year"][-1], orders["month"][-1], orders["date"][-1]]
    begindate = [int(x) for x in begindate[:]]
    enddate = [int(x) for x in enddate[:]]
    fileopen.close()
    symbols = list(set(orders["symbol"]))
    return orders, symbols, begindate, enddate


if __name__ == "__main__":
    if len(sys.argv) < 4:
        # print "Not sufficient arguments."
        # print "Arguments should be: [Starting Cash] [Order File] [Output File]"
        # Unit Test
        ls_keys = ["close"]
        filename = "orders.csv"
        output = "testoutput.csv"
        startingcash = 10000000
        orderbook, symbols, begin, end = parse_orders(filename)
        timestamps = get_timestamps(begin, end, symbols)
        mydata = get_data(timestamps,symbols,ls_keys)
    elif re.match("$[0-9]*^", sys.argv[1]):
        print "First argument must be an integer representing investable cash."
    else:
        startingcash = sys.argv[1]
        orderbook, symbols = parse_orders(sys.argv[2])
        outputfile = sys.argv[2]
        print symbols
