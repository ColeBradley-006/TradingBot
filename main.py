from datetime import datetime
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

def fiftyDayHigh(data):
    """
    Finds the highest close in the past two hundred days for stocks in list
    """
    highValues = []
    for array in data:
        highValues.append(max(array[:50]))
    return highValues

def fiftyDayLow(data):
    """
    This finds the low value in the past fifty days
    """
    lowValues = []
    for array in data:
        lowValues.append(min(array[:50]))
    return lowValues

def tenPrevFiftyDayAverages(data):
    """
    Calculates the last 10 50 day averages, so we can see if they are trending down or up
    This data will be helpful to determine watchlist stocks; are they getting closer to breaking above or below the
    200-day SMA
    """
    prevFiftyDayAverages = []
    for stock in data:
        stockFiftyDayAverages = []
        for i in range(10):
            sum = 0
            for j in range(50):
                sum += stock[j]
            stock.pop(0)
            stockFiftyDayAverages.append(sum/50)
        prevFiftyDayAverages.append(stockFiftyDayAverages)
    return prevFiftyDayAverages

def addToBuyList(high, low, ten, twoHundred):
    """
    This function will write to the buy list
    """
    above = True
    f = open(r"C:\Users\coleb\Desktop\Personal Projects\TradingBot\package\BuyList.txt", "w")
    if above:
        f.write("The 50 day SMA for " + "stockname" + " has moved above the 200 day SMA, " + "stock name" + " is now a recommended buy.\n")
        f.write("The data for " + "stock name" + " is as follows: \n")
        df = yf.download("aapl", start="2020-11-03", end="2022-01-17")
        np.savetxt(r"C:\Users\coleb\Desktop\Personal Projects\TradingBot\package\BuyList.txt", df.values, fmt="%d")
        # The above line is how dataframes can be written to text files in python
        # Write data about the stock to the file
    f.close()
    return

def addToSellList(high, low, ten, twoHundred):
    """
    This function will write to sell list
    """
    return

def addToWatchlist(high, low, ten, twoHundred):
    """
    This function will write to a watchlist
    """
    return

def calculateCross(ten, twoHundred):
    """
    This function will use the inputted direction based on if 10 day SMA is above or below 200 day SMA to determine
    if a cross has happened.
    """
    upCross = False
    downCross = False
    for i in range(1, 10):
        tenDay = ten[i]
        prevTenDay = ten[i - 1]
        if (twoHundred - tenDay) * (twoHundred - prevTenDay) < 0 and tenDay > twoHundred:
            upCross = True
        elif (twoHundred - tenDay) * (twoHundred - prevTenDay) < 0 and tenDay < twoHundred:
            downCross = True

    if upCross and downCross:
        return "both"
    elif upCross:
        return "buy"
    elif downCross:
        return "sell"

def fetchData(tickerList):
    """
    This function is built so we don't have to iterate through the data multiple times for each security.
    Gets data from the past 200 days
    """
    dataSet = []
    test = 0
    twoHundredDayAverages = []
    currentDate = str(datetime.date(datetime.now()))
    prevDate = currentDate[:3] + str(int(currentDate[3]) - 1) + currentDate[4:]
    for company in tickerList:
        test += 1
        dataPoints = []
        sum = 0
        data = yf.download(company, start=prevDate, end=currentDate).tail(200)
        closeData = data["Close"]
        dateData = data.index.values  # Fetches the date data for plotting, not necessary if not plotting
        for point in reversed(closeData):
            dataPoint = float(point)
            dataPoints.append(dataPoint)
            sum += dataPoint
        dataSet.append(dataPoints)
        twoHundredDayAverages.append(sum / 200)

        if test == 5:
            break

    listOfHighs = fiftyDayHigh(dataSet)
    listOfLows = fiftyDayLow(dataSet)
    listOfAverages = tenPrevFiftyDayAverages(dataSet)
    # Currently Calculating the 10 50 day averages from 210 days ago FIX!!!!

    return listOfHighs, listOfLows, listOfAverages, twoHundredDayAverages

def analyzeStocks():
    """
    Main Function
    """
    f = open(r"C:\Users\coleb\Desktop\Personal Projects\TradingBot\package\stockList.txt", "r", encoding="utf-16-le")
    stockList = f.read()
    stockList = stockList.split("\n")
    stockList = stockList[1:-1]
    f.close()

    high, low, fiftyDayMulti, twoHundredDay = fetchData(stockList)
    fiftyDay = []
    for each in fiftyDayMulti:
        fiftyDay.append(each[9])
    series = {"High": high, "Low": low, "10SMA": fiftyDay, "200SMA": twoHundredDay}
    summary = pd.DataFrame(data=series, index=stockList[:5]) #This will be used to return data on each of the
    addToBuyList(high, low, fiftyDay, twoHundredDay)
    addToSellList(high, low, fiftyDay, twoHundredDay)
    addToWatchlist(high, low, fiftyDay, twoHundredDay)

    """
    Might add some plotting capability, tbd
    """

"""
Runs Program
"""
analyzeStocks()