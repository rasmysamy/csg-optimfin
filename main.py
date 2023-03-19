import json

import yfinance
import helper
import requests
import pandas as pd


def optimalValueAlgorithm(symbols, prices_at_day, start_amount):
    # We then use dynamic programming in order to optimize transactions. We make a table for the maximal amount
    # Of cash or actions for either symbol or for cash ("CASH")

    # In other terms, we try to keep track of the maximum amount of any asset we can have on any given day, and the chain
    # of operations required to get there.
    # We know that this is guaranteed to be the best possible result, because this approach to the problem verifies the
    # local optimality condition for dynamic programming.
    days = len(prices_at_day[symbols[0]])
    print(days)
    elems = symbols + ["CASH"] # Our possible assets are either stocks or cash.

    optimal_portfolios = dict()
    for symbol in elems:
        optimal_portfolios[symbol] = [(0, None)] * days
    # We start by assuming we simply buy in the first day
    for sym in symbols:
        optimal_portfolios[sym][0] = (start_amount/prices_at_day[sym][0], [(start_amount/prices_at_day[sym][0], ("BUY", sym, 0))])
    optimal_portfolios["CASH"][0] = (start_amount, [])

    for i in range(1, days):
        # We can either sell and then hold "CASH":
        for sym in symbols:
            val_sell = optimal_portfolios[sym][i - 1][0] * prices_at_day[sym][i]
            val_keep = max(optimal_portfolios["CASH"][i - 1][0], optimal_portfolios["CASH"][i][0])
            # If we can generate more cash through selling these shares on this day than through
            # any other series of actions, we do so and add the sell action to the series of operations that led to the
            # generation of these shares.
            if val_sell > val_keep:
                optimal_portfolios["CASH"][i] = (val_sell, optimal_portfolios[sym][i-1][1] + [(val_sell, ("SELL", sym, i))])
            else:
                # We have to check whether it's optiomal to keep the previous cash balance or to sell another share
                if optimal_portfolios["CASH"][i][0] < optimal_portfolios["CASH"][i-1][0]:
                    optimal_portfolios["CASH"][i] = optimal_portfolios["CASH"][i-1]
        # We also see if the money we have now is enough to generate more shares than we could before
        for sym in symbols:
            val_keep = optimal_portfolios[sym][i-1][0]
            val_buy = optimal_portfolios["CASH"][i-1][0]/prices_at_day[sym][i]
            # If we don't get more shares, we just keep the same amount and the same chain of operations
            # otherwise, we update the number of shares, and add the buy action to the chain of operations
            # that led to our current cash balance.
            if val_buy > val_keep:
                optimal_portfolios[sym][i] = (val_buy, optimal_portfolios["CASH"][i-1][1] + [(val_buy, ("BUY", sym, i))])
            else:
                optimal_portfolios[sym][i] = optimal_portfolios[sym][i-1]

    return optimal_portfolios["CASH"][-1]


def main():
    #Fields related to API
    ID = "lespigeonniers"
    PASS = "lost-continent"
    api_endpoint = "https://api.csgames2023.sandbox.croesusfin.cloud/CroesusValidation"
    FinalValidationMode = "croesus-of-lydia"


    #Inputs of program
    symbols = ["GOOG", "AMZN", "META", "MSFT", "AAPL"]
    dateStart = "2023-01-01"
    dateEnd = "2023-02-02"
    startAmount = 1_000_000

    prices_at_day, df = helper.constructHistory(symbols, dateStart, dateEnd)
    print(prices_at_day)

    unparsedActions = optimalValueAlgorithm(symbols, prices_at_day, startAmount)
    #Hacky code to go from index to Date so we can format our JSON
    test = list(df['Open'].index)
    print(test)
    indexToDate = []

    for v in test:
        indexToDate.append(str(v)[:10])


    #Parsing our answer so we can transform into json
    result = helper.parseResult(unparsedActions[1], indexToDate)



    r = requests.post(url=api_endpoint, json=result, params={"TeamName": ID, "TeamPassword": PASS, "FinalValidationMode": FinalValidationMode})

if __name__ == "__main__":
    main()
