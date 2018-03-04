
from __future__ import print_function
import httplib2
import os

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
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive'
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
                                   'drive-python-quickstart.json')

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

def main():
    """Shows basic usage of the Google Drive API.

    Creates a Google Drive API service object and outputs the names and IDs
    for up to 10 files.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)

    results = service.files().list(
        pageSize=10,fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print('{0} ({1})'.format(item['name'], item['id']))


def makeSheet():
    """Shows basic usage of the Google Drive API.

    Creates a Google Drive API service object and outputs the names and IDs
    for up to 10 files.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)

    cryptoFolderId = '1iVlf0LJSpot0tB6ehbpnfYZ8IZ1VYPTK'

    file_metadata = {
        'name' : 'TestFiles!',
        'mimeType' : 'application/vnd.google-apps.spreadsheet',
        'parents': [cryptoFolderId] 
        }
    
    file = service.files().create(body=file_metadata,
                                    fields='id').execute()
    
    print(file.get('id'))

def checkForSheet():

    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)

    cryptoFolderId = '1iVlf0LJSpot0tB6ehbpnfYZ8IZ1VYPTK'

    results = service.files().list(
        q="name = 'TestFiles!' and '1iVlf0LJSpot0tB6ehbpnfYZ8IZ1VYPTK' in parents", pageSize=1000 ,fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print('{0} ({1})'.format(item['name'], item['id']))

#Returns sheetID
#Supply sheet name and Google folder ID
#Example mySheetTitle, 1iVlf0LJSpot0tB6ehbpnfYZ8IZ1VYPTK
def checkForSheetInFolder(sheetName, folderID):

    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)

    results = service.files().list(
        q="name = '" + sheetName + "' and '" + folderID + "' in parents",
        pageSize=1000 ,
        fields="nextPageToken, files(id, name)").execute()

    items = results.get('files', [])
    if not items:
        #return a blank string
        print('No files found.')
        return ''
    else:
        print('Files:')
        for item in items:
            print('{0} ({1})'.format(item['name'], item['id']))
    return items[0]['id']

def makeSheetInFolder(sheetName, folderID):

    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)

    file_metadata = {
        'name' : sheetName,
        'mimeType' : 'application/vnd.google-apps.spreadsheet',
        'parents': [folderID] 
        }
    
    file = service.files().create(body=file_metadata,
                                    fields='id').execute()
    print(file.get('id'))
    return file.get('id')

if __name__ == '__main__':
    #makeSheet()
    #newSheet = makeSheetInFolder('Mikes', '1iVlf0LJSpot0tB6ehbpnfYZ8IZ1VYPTK')
    #print(newSheet)
    #mySheet = checkForSheetInFolder('Mikess', '1iVlf0LJSpot0tB6ehbpnfYZ8IZ1VYPTK')
    #print('My sheet ID is: ', mySheet)
    print('Started')