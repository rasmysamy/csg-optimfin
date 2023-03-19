import yfinance as yf
import math
#import matplotlib.pyplot as plt

#Function that builds open price history of a tickers list
def constructHistory(tickerList, dateStart, dateEnd):
    openPriceHistory = {}
    for tickerName in tickerList:
        currTick = yf.Ticker(tickerName)
        df = currTick.history(start=dateStart, end=dateEnd)
        open_quote = df['Open']
        tmp = []
        for openPrice in open_quote:
            tmp.append(openPrice)
        openPriceHistory[tickerName] = tmp

    return openPriceHistory, df

#Arguments:
#unparsedActions: List of tuples, with second element having format (ACTION, TICKER, INDEX)
#indextoDate: List with i-th date as i-th value
#return : List of dictionnaries for JSON
def parseResult(unparsedActions, indexToDate):
    result = []

    for v in unparsedActions:
        tmp = {}
        #We have the indexes of our action, so we convert to date
        tmp["date"] = indexToDate[v[1][2]]
        tmp["action"] = v[1][0]
        tmp["ticker"] = v[1][1]
        result.append(tmp)

    return result

