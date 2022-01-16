import numpy as np
import pandas as pd
import matplotlib as mp
import yfinance as yf

"""
This project can be run every day after market close and it will return:
    -A buy List
    -A sell List
    -An updated watchlist
This is for all of the 100 largest market caps stocks on the NYSE and personally held securities.
These lists are based off of the golden cross, the death cross, and whether assets are approaching these two events
"""

def zero_division(a, b):
    """
    This makes sure the program doesn't crash by attempting to divide by 0
    """
    return a / b if b != 0 else 0




def createSymbolsList(inputData, outputData):
    """
    This Function will create a list of tickers from stockList provided
    """
    for line in inputData:
        title = str(line).upper()
        ticker = yf.Ticker(title)
        exec(title + " = ticker")
        outputData.append(title)
    return outputData

def fiftyDayHigh(symbol):
    """
    Finds the highest close in the past fifty days for stocks in list
    """
    return


def twoHundredDayAverage(symbol):
    return


def tenPrevFiftyDayAverages(symbol):
    return


def addToBuyList(symbol):
    return


def addToSellList(symbol):
    return


def buyListReturn():
    return


def sellListReturn():
    return


def watchlistReturn():
    return


def analyzeStocks():
    """
    Main Function
    """
    f = open(r"C:\Users\coleb\Desktop\Personal Projects\TradingBot\package\stockList.txt", "r", encoding="utf-16-le")
    stockList = f.read()
    stockList = stockList.split("\n")
    stockList = stockList[1:-1]
    symbolList = []
    tickerList = createSymbolsList(stockList, symbolList)


analyzeStocks()

