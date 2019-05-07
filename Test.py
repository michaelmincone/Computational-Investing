from tkinter import *
import pandas as pd
import csv
#import tulipy as ti
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
from pandas._libs import json
'''
ts = TimeSeries(key='5OOTS0NZHCYN4TCE', output_format='pandas')
ti = TechIndicators(key='5OOTS0NZHCYN4TCE')

def getRSI(symbol):
    rsi = ti.get_rsi(symbol=symbol, interval="daily", series_type="close")  # returns RSI as JSON data
    with open('rsi.json', 'w') as outfile:
        json.dump(rsi, outfile)

    inputFile = open('rsi.json') #open json file
    outputFile = open('RSI.csv', 'w') #load csv file
    data = json.load(inputFile) #load json content
    inputFile.close() #close the input file
    output = csv.writer(outputFile) #create a csv.write
    output.writerow(data[0].keys())  # header row

    for row in data:
        output.writerow(row.values()) #values row

    lst = []
    with open('RSI.csv', 'r') as f:
        reader = csv.reader(f)
        lst = list(reader)  #reads csv file into a list

    split = (lst[2][0]).split(': ') #gets first rsi value ands splits by ": "  EX: "{"RSI": "69.7248"}" is now ["{"RSI"", "69.7248"}"]
    rsiStr = split[1] #gets the second value from previous array EX: "69.7248"}"
    rsival = rsiStr[1:len(rsiStr)-2] #Parses substring to get actual string value  EX: 69.7248
    rsival = float(rsival) #converts the string to float

    return rsival

def getMACD(macd):

    with open('macd.json', 'w') as outfile:
        json.dump(macd, outfile)

    inputFile = open('macd.json') #open json file
    outputFile = open('MACD.csv', 'w') #load csv file
    data = json.load(inputFile) #load json content
    inputFile.close() #close the input file
    output = csv.writer(outputFile) #create a csv.write
    output.writerow(data[0].keys())  # header row

    for row in data:
        output.writerow(row.values()) #values row

    lst = []
    with open('MACD.csv', 'r') as f:
        reader = csv.reader(f)
        lst = list(reader)  #reads csv file into a list

    macd = 0
    macdHist = 0
    macdSignal = 0
    split = (lst[2][0]).split(', ')

    first = split[0]
    first = first.split(': ')
    name = first[0]
    val = first[1]
    name = name[2:len(name) - 1]
    if name == 'MACD':
        macd = val[1:len(val) - 1]


    elif name == 'MACD_Signal':
        macdSignal = val[1:len(val) - 1]


    elif name == 'MACD_Hist':
        macdHist = val[1:len(val) - 1]


    second = split[1]
    second = second.split(': ')
    name = second[0]
    val = second[1]
    name = name[1:len(name) - 1]
    if name == 'MACD':
        macd = val[1:len(val) - 1]

    elif name == 'MACD_Signal':
        macdSignal = val[1:len(val) - 1]

    elif name == 'MACD_Hist':
        macdHist = val[1:len(val) - 1]



    third = split[2]
    third = third.split(': ')
    name = third[0]
    val = third[1]
    name = name[1:len(name) - 1]
    if name == 'MACD':
        macd = val[1:len(val) - 2]



    elif name == 'MACD_Signal':
        macdSignal = val[1:len(val) - 2]



    elif name == 'MACD_Hist':
        macdHist = val[1:len(val) - 2]


    return (macd, macdSignal, macdHist)

def evaluate(event):
        macd = ti.get_macd(symbol=entry.get(), interval="daily", series_type="close", fastperiod=10, slowperiod=20, signalperiod=50)  # returns MACD as JSON data
        vals102050 = getMACD(macd)
        macd200 = ti.get_macd(symbol=entry.get(), interval="daily", series_type="close", fastperiod=10, slowperiod=20, signalperiod=200)  # returns MACD as JSON data
        vals1020200 = getMACD(macd200)
        rsi = getRSI(entry.get())
        res.configure(text="RSI of " + str(entry.get()) + " is " + str(rsi) + "\n" +
                           "MACD (10, 20, 50) is " + str(vals102050[0]) + "\n" +
                           "MACD Signal (10, 20, 50) is " + str(vals102050[1]) + "\n" +
                           "MACD Histogram (10, 20, 50) is " + str(vals102050[2]) + "\n" +
                           "MACD (10, 20, 200) is " + str(vals1020200[0]) + "\n" +
                           "MACD Signal (10, 20, 200) is " + str(vals1020200[1]) + "\n" +
                           "MACD Histogram (10, 20, 200) is " + str(vals1020200[2]))

w = Tk()
w.geometry("300x200")
Label(w, text="Enter a stock:").pack()
entry = Entry(w)

entry.bind("<Return>", evaluate)
entry.pack()
res = Label(w)
res.pack()
w.mainloop()   '''

import http.client
connection = http.client.HTTPSConnection('sandbox.tradier.com', 443, timeout = 30)

headers = {"Accept":"application/json",
           "Authorization":"Bearer YbIFB1EU8qOKo8SZ7aSiLdd3PMSr"}

def getExpirations(symbol):
    connection.request('GET', '/v1/markets/options/expirations?symbol=' + symbol, None, headers)
    response = connection.getresponse()
    expirations = response.read()

    df = pd.read_json(expirations)
    df.to_csv("expirations.csv")

    with open('expirations.csv') as f:
        s = f.read() + '\n' # add trailing new line character

    elst = s.split(", ")
    elst.pop(0)
    expirationlst = []

    for x in elst:
        tmp = x.split("'")[1]
        expirationlst.append(tmp)
    return expirationlst


def getOptionsChain(date):
    connection.request('GET', '/v1/markets/options/chains?symbol=msft&expiration=' + date, None, headers)
    response = connection.getresponse()
    optioninfo = response.read()

    df = pd.read_json(optioninfo)
    df.to_csv("info.csv")

    with open('info.csv') as f:
        s = f.read() + '\n' # add trailing new line character

    lst = s.split(", ")
    finalLst = []

    while len(lst) > 0:
        tmp = []
        for i in range(0,34):
            tmp.append(lst[0])
            lst.pop(0)
        finalLst.append(tmp)

    end = []
    for x in finalLst:
        price = x[1]
        price = price.split(": ")[1]

        type = price.split(" ")[5]
        type = type[:-1]

        price = price.split(" ")[4]
        price = float(price[1:])

        last = x[4]
        last = last.split(": ")[1]
        if last != "None":
            last = float(last)

        bid = x[11]
        bid = bid.split(": ")[1]
        bid = float(bid)

        ask = x[12]
        ask = ask.split(": ")[1]
        ask = float(ask)

        strike = x[14]
        strike = strike.split(": ")[1]
        strike = float(strike)

        info = {
            "price": price,
            "type": type,
            "last": last,
            "bid": bid,
            "ask": ask,
            "strike": strike
        }
        end.append(info)
    return end


myLst = getExpirations("AAPL") # list of options expiration dates
options = getOptionsChain(myLst[0]) #list of option chains at a certain expiration date
print(options)

