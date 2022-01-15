import numpy as np
import pandas as pd
import matplotlib as mp
import yfinance as yf


# This makes sure the program doesn't crash by attempting to divide by 0
def zero_division(a, b):
    return a / b if b != 0 else 0


if __name__ == '__main__':
    print("Cool")
