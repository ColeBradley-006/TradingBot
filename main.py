import timeit

import matplotlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

"""
This project can be run every day after market close and it will return:
    -A buy List
    -A sell List
    -An updated watchlist
This is for all of the 100 largest market caps stocks on the NYSE and personally held securities.
These lists are based off of the golden cross, the death cross, and whether assets are approaching these two events
"""

def createSymbolsList(inputData):
    """
    This Function will create a dictionary of tickers from the stockList provided
    A dictionary was selected for easy access to different variables
    """
    outputData = []
    for line in inputData:
        yf.Ticker(line)
        outputData.append(line)
    return outputData

def fiftyDayHigh(data):
    """
    Finds the highest close in the past two hundred days for stocks in list
    """
    highValues = []
    for array in data:
        highValues.append(max(array[:50]))
    return highValues

def fiftyDayLow(data):
    lowValues = []
    for array in data:
        lowValues.append(min(array[:50]))
    return lowValues
def tenPrevFiftyDayAverages(data):
    """
    Calculates the last 10 10 day averages, so we can see if they are trending down or up
    This data will be helpful to determine watchlist stocks; are they getting closer to breaking above or below the
    200 day SMA
    """
    prevTenDayAverages = []
    for stock in data:
        stockTenDayAverages = []
        for i in range(10):
            count = 0
            sum = 0
            for point in reversed(stock):
                count += 1
                sum += point
                if count == 10:
                    stock.pop()
                    stockTenDayAverages.append(sum/10)
                    break
        prevTenDayAverages.append(stockTenDayAverages)

    return prevTenDayAverages


def addToBuyList(symbol):
    """
    This function determines if the
    """

    return

def addToSellList(symbol):
    return


def buyListReturn():
    return


def sellListReturn():
    return


def watchlistReturn():
    return

def fetchData(tickerList):
    """
    This function is built so we don't have to iterate through the data multiple times for each security.
    Gets data from the past 200 days
    """
    dataSet =[]
    test = 0
    twoHundredDayAverages = []
    for company in tickerList:
        test += 1
        dataPoints =[]
        sum = 0
        count = 0
        data = yf.download(company, start="2020-11-03", end="2022-01-17")
        closeData = data["Close"]
        for point in reversed(closeData):
            dataPoint = float(point)
            dataPoints.append(dataPoint)
            sum += dataPoint
            count += 1
            if count == 200:
                dataSet.append(dataPoints)
                twoHundredDayAverages.append(sum / 200)
                break

        if test == 5:
            break

    listOfHighs =fiftyDayHigh(dataSet)
    listOfLows = fiftyDayLow(dataSet)
    listOfAverages = tenPrevFiftyDayAverages(dataSet)

    return listOfHighs, listOfLows, listOfAverages, twoHundredDayAverages

def analyzeStocks():
    """
    Main Function
    """
    f = open(r"C:\Users\coleb\Desktop\Personal Projects\TradingBot\package\stockList.txt", "r", encoding="utf-16-le")
    stockList = f.read()
    stockList = stockList.split("\n")
    stockList = stockList[1:-1]
    tickerList = createSymbolsList(stockList)
    high, low, tenDay, twoHundredDay = fetchData(tickerList)

    #data['Adj Close'].plot()
    #plt.show()


analyzeStocks()

