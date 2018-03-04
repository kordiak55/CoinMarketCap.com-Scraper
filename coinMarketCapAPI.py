import urllib.request as myRequest
import json
import datetime
#import requests - Not needed, errors on Pi
import googleSheet
import googleDriveAPI
from pprint import pprint

#What we have to do....
#1 get data
#2 loop through datas
#3 see if worbook/sheetexists
#4 if exist, open and append
#5 if doesn't exist, create it, then do step 4


def getCoinData():
    myLink = 'https://api.coinmarketcap.com/v1/ticker/'
    myFolder = '1iVlf0LJSpot0tB6ehbpnfYZ8IZ1VYPTK'

    myData = myRequest.urlopen(myLink)
    myJson = json.loads(myData.read().decode())

    print(myJson[0]['name'])

    #header for any new sheets...
    coinTabHeader = {'24h_volume_usd': '24h_volume_usd',
                     'available_supply': 'available_supply',
                     'id': 'id',
                     'last_updated': 'last_updated',
                     'market_cap_usd': 'market_cap_usd',
                     'max_supply': 'max_supply',
                     'name': 'name',
                     'percent_change_1h': 'percent_change_1h',
                     'percent_change_24h': 'percent_change_24h',
                     'percent_change_7d': 'percent_change_7d',
                     'price_btc': 'price_btc',
                     'price_usd': 'price_usd',
                     'rank': 'rank',
                     'symbol': 'symbol',
                     'total_supply': 'total_supply',
                     'date': 'date',
                     'year': 'year',
                     'month': 'month',
                     'day': 'day',
                     'day_of_week': 'day_of_week',
                     'time': 'time',
                     'hour': 'hour',
                     'minute': 'minute'}

    #Add some more stuff into our data set so we dont have to calcualte it on the sheet
    #mostly date/time stuff, days, hours, mins, week day, etc.
    for coin in myJson:

        timeFixer = datetime.datetime.fromtimestamp(
            int(coin['last_updated']))

        coin["date"] = timeFixer.date().strftime('%Y-%m-%d')
        coin["year"] = timeFixer.date().year
        coin["month"] = timeFixer.date().month
        coin["day"] = timeFixer.date().day
        #Monday is 0 and Sunday is 6.
        coin["day_of_week"] = timeFixer.date().weekday()
        coin["time"] = timeFixer.time().strftime('%H:%M:%S')
        coin["hour"] = timeFixer.time().hour
        coin["minute"] = timeFixer.time().minute

    #Loop through each coin and add to your google drive
    for coin in myJson:
        
        #check if the there is a sheet already created for the coin in /crypto
        #if there is, it will return the sheet ID, if not it will return None
        mySheetID = googleDriveAPI.checkForSheetInFolder(coin["name"], myFolder)

        if mySheetID is '':
            #No sheet found, try and make a sheet, return the new sheets ID
            mySheetID = googleDriveAPI.makeSheetInFolder(coin["name"], myFolder)
            response = googleSheet.appendRowToSheet(mySheetID, coinTabHeader)
        
            #worksheet ID was found, do nothing.
        
        #log data into sheet
        response = googleSheet.appendRowToSheet(mySheetID, coin)


        #googleSheet.logDataToGoogle(coin["name"], coin)



    pprint([coin])


#run
getCoinData()