import csv
from datetime import datetime
import os
from dotenv import load_dotenv
import requests

ALPHA_VINTAGE_API = 'ALPHA_VINTAGE_API'

# take environment variables from .env.
load_dotenv()


import Utils

directoryToSaveData = 'data'

def entry():
    fileNameForCSV = 'stocksData'
    dateToday = datetime.today().strftime("%Y-%m-%d")
    fileNameForCSV = directoryToSaveData + "/" + fileNameForCSV + "_" + dateToday + ".csv"

    stockList = ['MSFT', 'AAPL', 'NVDA', 'AMZN', 'GOOG', 'META', 'TSLA', 'AMD', 'CRM', 'BABA', 'INTC', 'PYPL', 'TTD', 'EA', 'ZG', 'MTCH', 'YELP']
    for stockName in stockList:
        stockToLook = stockName
        stockDetails = getValueFromAPI(stockToLook)
        writeToCSVCallAndResponse = writeToCSV(fileNameForCSV, stockDetails)
        print ("File writing to CSV: ", writeToCSVCallAndResponse)

    print (":::Process finished:::")



def getValueFromAPI(stockSymbol):
    urlAlphaVintage = "https://www.alphavantage.co/query?function=OVERVIEW&symbol="+ stockSymbol + "&apikey=" + os.getenv(ALPHA_VINTAGE_API)
    responseFromAPI = requests.get(urlAlphaVintage)
    response = responseFromAPI.json()

    #response is dict
    return response


def writeToCSV(fileName, objectToWrite):
    # see if file exists or not
    # if not, add the first line which is all the keys for
    # then parse over the values as seperate rows

    rowToWrite = []
    if (not Utils.checkIfFileExists(fileName)):
        with open(fileName, 'w', newline='') as file:
            writer = csv.writer(file)
            for key in objectToWrite:
                rowToWrite.append(key)
            writer.writerow(rowToWrite)

    with open(fileName, 'a', newline='') as file:
        rowToWrite = []
        writer = csv.writer(file)
        # save the values only now
        for key in objectToWrite:
            rowToWrite.append(objectToWrite[key])
        writer.writerow(rowToWrite)


    return True



if __name__ == '__main__':
    entry()

