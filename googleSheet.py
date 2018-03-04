from __future__ import print_function
import httplib2
import os

from googleapiclient import discovery

from pprint import pprint
from googleapiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage


try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Python'

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

#Authenicate
credentials = get_credentials()
http = credentials.authorize(httplib2.Http())
discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                'version=v4')
service = discovery.build('sheets', 'v4', http=http,
                            discoveryServiceUrl=discoveryUrl)

#spreadsheet_id = '1TvDIEhphJpGPJoGFql2MbwXF9RkqBVcxhi2B8oDckm0'

def tester():
    """
    BEFORE RUNNING:
    ---------------
    1. If not already done, enable the Google Sheets API
    and check the quota for your project at
    https://console.developers.google.com/apis/api/sheets
    2. Install the Python client library for Google APIs by running
    `pip install --upgrade google-api-python-client`
    """

    # TODO: Change placeholder below to generate authentication credentials. See
    # https://developers.google.com/sheets/quickstart/python#step_3_set_up_the_sample
    #
    # Authorize using one of the following scopes:
    #     'https://www.googleapis.com/auth/drive'
    #     'https://www.googleapis.com/auth/drive.file'
    #     'https://www.googleapis.com/auth/spreadsheets'
    credentials = get_credentials()

    service = discovery.build('sheets', 'v4', credentials=credentials)

    spreadsheet_id = '1TvDIEhphJpGPJoGFql2MbwXF9RkqBVcxhi2B8oDckm0'

    # The A1 notation of a range to search for a logical table of data.
    # Values will be appended after the last row of the table.
    range_ = 'Sheet3!A1:D5'  # TODO: Update placeholder value.

    # How the input data should be interpreted.
    value_input_option = 'USER_ENTERED'  # TODO: Update placeholder value.

    # How the input data should be inserted.
    insert_data_option = 'INSERT_ROWS'  # TODO: Update placeholder value.

    value_range_body = {
        "majorDimension": "ROWS",
        "values": [
            ["Item", "Cost", "Stocked", "Ship Date"],
            ["Wheel", "$20.50", "4", "3/1/2016"],
            ["Door", "$15", "2", "3/15/2016"],
            ["Engine", "$100", "1", "30/20/2016"],
            ["Totals", "=SUM(B2:B4)", "=SUM(C2:C4)", "=MAX(D2:D4)"]
        ],
    }

    request = service.spreadsheets().values().append(spreadsheetId=spreadsheet_id, range=range_, valueInputOption=value_input_option, insertDataOption=insert_data_option, body=value_range_body)

    response = request.execute()

    # TODO: Change code below to process the `response` dict:
    pprint(response)                           

def main():
    """Shows basic usage of the Sheets API.

    Creates a Sheets API service object and prints the names and majors of
    students in a sample spreadsheet:
    https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    spreadsheetId = '1TvDIEhphJpGPJoGFql2MbwXF9RkqBVcxhi2B8oDckm0'
    rangeName = 'testSheet!A2:E'
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        print('Name, Major:')
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print('%s, %s' % (row[0], row[1]))

def sheetExists(sheetName):    
    #Try to get value from sheet, if failed, return fasle. Assume sheet does not exist.
    try:
        rangeName = sheetName
        rangeName += '!A1'
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id, range=rangeName).execute()
        values = result.get('values', [])        
        return True

    except:
        #No sheet found
        return False

def createNewSheet(sheetName):

    batch_update_spreadsheet_request_body = {
        # A list of updates to apply to the spreadsheet.
        # Requests will be applied in the order they are specified.
        # If any request is not valid, no requests will be applied.
        'requests': [{'addSheet':{'properties':{'title': sheetName}} }],

    }

    request = service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body=batch_update_spreadsheet_request_body)
    response = request.execute()
    #pprint(response)

def appendData(sheetName, row):

    #start point of table to append to, dimmention not required 
    sheetName += '!A1:A1'

    range_ = sheetName

    # How the input data should be interpreted.
    value_input_option = 'USER_ENTERED' 

    # How the input data should be inserted.
    insert_data_option = 'INSERT_ROWS'

    # value_range_body = {
    #     "majorDimension": "ROWS",
    #     "values": [
    #         [row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14]],
    #     ],
    # }

    value_range_body = {
        "majorDimension": "ROWS",
        "values": [
            [row['24h_volume_usd'],
             row['available_supply'],
             row['id'],
             row['last_updated'],
             row['market_cap_usd'],
             row['max_supply'],
             row['name'],
             row['percent_change_1h'],
             row['percent_change_24h'],
             row['percent_change_7d'],
             row['price_btc'],
             row['price_usd'],
             row['rank'],
             row['symbol'],
             row['total_supply'],
             row["date"],
             row["year"],
             row["month"],
             row["day"],
             #Monday is 0 and Sunday is 6.
             row["day_of_week"],
             row["time"],
             row["hour"],
             row["minute"]],
        ],
    }

    request = service.spreadsheets().values().append(spreadsheetId=spreadsheet_id, range=range_, valueInputOption=value_input_option, insertDataOption=insert_data_option, body=value_range_body)
    response = request.execute()
    print(response)     
    return response

def logDataToGoogle(sheetName, dataSet):

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

    myCoinDataRow = dataSet
    mySheetName = sheetName
    
    try: 
        appendData(mySheetName, myCoinDataRow)
        print(mySheetName, ' appended.')
    except Exception as e:
        print(e)
        #print('Appending ', myCoinDataRow, ' data set to ', mySheetName, ' failed. Trying to create new sheet...')
        try:
            createNewSheet(mySheetName)
            appendData(mySheetName, coinTabHeader)            
            appendData(mySheetName, myCoinDataRow)
            print('Created sheet: ', mySheetName, ' and appended: ', myCoinDataRow)
        except:
            print('Could not append to ', mySheetName)

def appendRowToSheet(sheetId, row):

    #default sheet name value
    tabName = 'Sheet1'

    #start point of table to append to, dimmention not required 
    tabName += '!A1:A1'

    #values for API
    range_ = tabName
    spreadsheet_id = sheetId

    # How the input data should be interpreted.
    value_input_option = 'USER_ENTERED' 

    # How the input data should be inserted.
    insert_data_option = 'INSERT_ROWS'

    value_range_body = {
        "majorDimension": "ROWS",
        "values": [
            [row['24h_volume_usd'],
             row['available_supply'],
             row['id'],
             row['last_updated'],
             row['market_cap_usd'],
             row['max_supply'],
             row['name'],
             row['percent_change_1h'],
             row['percent_change_24h'],
             row['percent_change_7d'],
             row['price_btc'],
             row['price_usd'],
             row['rank'],
             row['symbol'],
             row['total_supply'],
             row["date"],
             row["year"],
             row["month"],
             row["day"],
             #Monday is 0 and Sunday is 6.
             row["day_of_week"],
             row["time"],
             row["hour"],
             row["minute"]],
        ],
    }

    request = service.spreadsheets().values().append(spreadsheetId=spreadsheet_id, range=range_, valueInputOption=value_input_option, insertDataOption=insert_data_option, body=value_range_body)
    response = request.execute()
    print(response)     
    return response

#Use this to append data to a google sheet AKA worksheet, not a tab
def appendDataToSheet(sheetID, dataSet):

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

    myCoinDataRow = dataSet
    #mySheetName = sheetName
    
    try: 
        appendData(mySheetName, myCoinDataRow)
        print(mySheetName, ' appended.')
    except Exception as e:
        print(e)
        #print('Appending ', myCoinDataRow, ' data set to ', mySheetName, ' failed. Trying to create new sheet...')
        try:
            createNewSheet(mySheetName)
            appendData(mySheetName, coinTabHeader)            
            appendData(mySheetName, myCoinDataRow)
            print('Created sheet: ', mySheetName, ' and appended: ', myCoinDataRow)
        except:
            print('Could not append to ', mySheetName)

if __name__ == '__main__':
    #main()
    #tester()
    #print(sheetExists('testSheet'))
    #createNewSheet('tester')
    print('Started')
