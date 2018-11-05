import pygsheets
from oauth2client.service_account import ServiceAccountCredentials
import traceback
import os
from .credentials import drive_api, drive_api2

def create_client(oauth2): 

    if oauth2:
        
        scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(drive_api2, scope)
        gc = pygsheets.authorize(credentials=creds,no_cache=True)

    else:
        
        f = open("client_secret.json","w+")
        f.write(str(drive_api))
        f.close()
        gc = pygsheets.authorize(outh_file='client_secret.json')
        os.remove('client_secret.json')
    
    return gc

def find_worksheet(sh,sheet):
    if sheet==None:
        wks = sh.sheet1
    elif type(sheet)==type(1):
        wks = sh.worksheet('index',sheet-1)
    elif type(sheet)==type('name'):
        wks = sh.worksheet('title',sheet)
    else:
        raise ValueError('Please specify "sheet" in integer or string')
    
    return wks

def readGs(file_name, sheet=None, header=True, oauth2 = True):
    """
        createGs(df, file_name, email_address, role='writer') : create spreadsheet file_name, write df pandas DataFrame, and share to email_address
        Notes for oauth2
        - if you use readGs make sure you have shared the spreadsheet with this email address (781154015913-compute@developer.gserviceaccount.com) (Top Right > Share > Enter Email).
        - param sheet accept integer or string. integer represents the position of worksheet in spreadsheet (1-based). string represent the name of worksheet. if sheet = None, then Sheet1 will be selected
        - Fill null columns. example : df = df.fillna('')
    """
    from pandas import DataFrame
    
    gc = create_client(oauth2 = oauth2)
    sh = gc.open(file_name)
    
    wks = find_worksheet(sh,sheet)
    
    values = wks.get_all_values(returnas='matrix', include_empty=False)
    values = [val for val in values if val!=[]]
    
    if header:
        keys = values[0]
        values = [row[:len(values[0])] for row in values[1:]]
        df = DataFrame(values, columns=keys)
    else:
        df = DataFrame(values)
    
    #drop column with no header
    try:
        df = df.drop('',axis=1)
    except:
        pass
        
    return df