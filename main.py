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

def addToBuyList(file, current, symbol, data):
    """
    This function will write to the buy list, stocks where the 50 day SMA passes above the 200 day SMA
    """

    file.write("The 50 day SMA for " + symbol + " has moved above the 200 day SMA, " + symbol + " is now a recommended buy.\n")
    file.write("The data for " + symbol + " is as follows: \n")
    file.write("Current: \t High: \t Low: \t 50 Day SMA: \t 200 Day SMA:\n")
    file.write(str(current) + "\t" + str(data.High[symbol]) + "\t" + str(data.Low[symbol]) + "\t" + str(
        data.FiftySMA[symbol]) + "\t" + str(data.TwoHundredSMA[symbol]) + "\n\n")

def addToSellList(file, current, symbol, data):
    """
    This function will write to sell list, stocks where the 50 day SMA passes below the 200 day SMA
    """
    file.write("The 50 day SMA for " + symbol + " has moved below the 200 day SMA, " + symbol + " is now a recommended sell.\n")
    file.write("The data for " + symbol + " is as follows: \n")
    file.write("Current: \t High: \t Low: \t 50 Day SMA: \t 200 Day SMA:\n")
    file.write(str(current) + "\t" + str(data.High[symbol]) + "\t" + str(data.Low[symbol]) + "\t" + str(
        data.FiftySMA[symbol]) + "\t" + str(data.TwoHundredSMA[symbol]) + "\n\n")

def addToWatchlist(file, current, symbol, data):
    """
    This function will write to a watchlist where the 50 day SMA is fluctuating above and below the 200 day SMA
    """
    file.write("The 50 day SMA for " + symbol + " has moved above and below the 200 day SMA, " + symbol + " is now recommended to observe.\n")
    file.write("The data for " + symbol + " is as follows: \n")
    file.write("Current: \t High: \t Low: \t 50 Day SMA: \t 200 Day SMA:\n")
    file.write(str(current) + "\t" + str(data.High[symbol]) + "\t" + str(data.Low[symbol]) + "\t" + str(
        data.FiftySMA[symbol]) + "\t" + str(data.TwoHundredSMA[symbol]) + "\n\n")


def addToHigherList(file, current, symbol, data):
    """
    This function will write to a list of stocks where the 50 day SMA is above the 200 day SMA
    """
    file.write("The 50 day SMA for " + symbol + " is above the 200 day SMA, " + symbol + " is potentially a sell.\n")
    file.write("The data for " + symbol + " is as follows: \n")
    file.write("Current: \t High: \t Low: \t 50 Day SMA: \t 200 Day SMA:\n")
    file.write(str(current) + "\t" + str(data.High[symbol]) + "\t" + str(data.Low[symbol]) + "\t" + str(data.FiftySMA[symbol]) + "\t" + str(data.TwoHundredSMA[symbol]) + "\n\n")


def addToLowerList(file, current, symbol, data):
    """
    This function will write to a list of stocks where the 50 day SMA is below the 200 day SMA
    """
    file.write("The 50 day SMA for " + symbol + " is below the 200 day SMA, " + symbol + " this is a potential buy.\n")
    file.write("The data for " + symbol + " is as follows: \n")
    file.write("Current: \t High: \t Low: \t 50 Day SMA: \t 200 Day SMA:\n")
    file.write(str(current) + "\t" + str(data.High[symbol]) + "\t" + str(data.Low[symbol]) + "\t" + str(data.FiftySMA[symbol]) + "\t" + str(data.TwoHundredSMA[symbol]) + "\n\n")


def calculateCross(ten, twoHundred):
    """
    This function will use the inputted direction based on if 10 day SMA is above or below 200 day SMA to determine
    if a cross has happened.
    """
    upCross = False
    downCross = False
    for i in range(8,-1, -1):
        tenDay = ten[i]
        prevTenDay = ten[i + 1]
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
    else:
        if ten[0] < twoHundred:
            return "lower"
        else:
            return "higher"

def fetchData(tickerList):
    """
    This function is built so we don't have to iterate through the data multiple times for each security.
    Gets data from the past 200 days
    """
    dataSet = []
    twoHundredDayAverages = []
    currentDate = str(datetime.date(datetime.now()))
    prevDate = currentDate[:3] + str(int(currentDate[3]) - 1) + currentDate[4:]
    for company in tickerList:
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

    listOfHighs = fiftyDayHigh(dataSet)
    listOfLows = fiftyDayLow(dataSet)
    listOfAverages = tenPrevFiftyDayAverages(dataSet)
    current = []
    for each in dataSet:
        current.append(each[0])

    return current, listOfHighs, listOfLows, listOfAverages, twoHundredDayAverages

def analyzeStocks():
    """
    Main Function, After collecting the data, writes to the files
    """
    f = open(r"C:\Users\coleb\Desktop\Personal Projects\TradingBot\package\stockList.txt", "r", encoding="utf-16-le")
    stockList = f.read()
    stockList = stockList.split("\n")
    stockList = stockList[1:-1]
    f.close()

    current, high, low, fiftyDayMulti, twoHundredDay = fetchData(stockList)
    fiftyDay = []
    for each in fiftyDayMulti:
        fiftyDay.append(each[0])
    series = {"High": high, "Low": low, "FiftySMA": fiftyDay, "TwoHundredSMA": twoHundredDay}
    summary = pd.DataFrame(data=series, index=stockList[:]) # This will be used to return data on each of the stocks
    status = []

    for i in range(len(stockList)):
        status.append(calculateCross(fiftyDayMulti[i], twoHundredDay[i]))

    # Creates all the files
    currentDate = str(datetime.date(datetime.now()))
    b = open(currentDate + "BuyList.txt", "w+")
    s = open(currentDate + "SellList.txt", "w+")
    w = open(currentDate + "WatchList.txt", "w+")
    h = open(currentDate + "HigherList.txt", "w+")
    l = open(currentDate + "LowerList.txt", "w+")
    b.write("Buy List for the Date: " + currentDate + "\n\n")
    s.write("Sell List for the Date: " + currentDate + "\n\n")
    w.write("Watch List for the Date: " + currentDate + "\n\n")
    h.write("Higher List for the Date: " + currentDate + "\n\n")
    l.write("Lower List for the Date: " + currentDate + "\n\n")
    for i in range(len(status)):
        symbol = stockList[i]
        stockSummary = summary.head(1)
        summary = summary.drop(summary.index[0])
        currentValue = current[i]
        position = status[i]
        if position == "buy":
            addToBuyList(b, currentValue, symbol, stockSummary)
        elif position == "sell":
            addToSellList(s, currentValue, symbol, stockSummary)
        elif position == "both":
            addToWatchlist(w, currentValue, symbol, stockSummary)
        elif position == "lower":
            addToLowerList(l, currentValue, symbol, stockSummary)
        else:
            addToHigherList(h, currentValue, symbol, stockSummary)

    b.close()
    s.close()
    w.close()
    h.close()
    l.close()
    """
    Might add some plotting capability, tbd
    """

"""
Runs Program
"""
analyzeStocks()