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

def readGs(file_name, sheet=None, header=True, oauth2 = None):
    """
        writeGs(df, file_name, sheet=None, row = 1, col=1, add_worksheet=False, worksheet_title=None) 
        createGs(df, file_name, email_address, role='writer') : create spreadsheet file_name, write df pandas DataFrame, and share to email_address
        
        notes on oauth2: 
        - the basic config for the authentification is true so it's using the drive_api2 for the connection, therefore it
        s required to share the spreadsheet into this certain project email: data-id-grab@quickstart-1538723811950.iam.gserviceaccount.com
        Follow this step to share the email: (Top Right > Share > Enter Email).
        - Param sheet accept integer or string. integer represents the position of worksheet in spreadsheet (1-based). string represent the name of worksheet. if sheet = None, then Sheet1 will be selected
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

def writeGs(df, file_name, sheet=None, row = 1, col=1, add_worksheet=False, worksheet_title=None, oauth2= None):

    gc = create_client(oauth2)
    sh = gc.open(file_name)
    
    if add_worksheet:
        if type(worksheet_title)!=type('title') or worksheet_title=='':
            raise ValueError('worksheet_title must in string form')
        else:
            wks = sh.add_worksheet(worksheet_title)
    else:
        wks = find_worksheet(sh,sheet)
    
    wks.clear()
    print('Writing DataFrame...')
    wks.set_dataframe(df,(row,col))
    print('Done writing')

def shareGs(file_name, email_address, role): 

    gc = create_client(oauth2=None)
    sh = gc.open(file_name)
    roles = ['writer','reader']
    if role not in  roles:
        raise ValueError('role must \'writer\' or \'reader\'\nFile not shared')
        
    sh.share(email_address,role)
    print('Shared')

def createGs(df, file_name, sheet=None, oauth2 = None , row = 1, col=1, add_worksheet=False, worksheet_title=None):

    gc = create_client(oauth2)
    file_exist = 0
    try:
        sh = gc.open(file_name)
        file_exist = 1
    except:
        sh = gc.create(file_name)
    
    if file_exist:
        raise ValueError('File already exist. If you want to overwrite the file, use writeGs. If you want to append the DataFrame, use insertGs.')

    writeGs(df, file_name)
    shareGs(file_name, email_address, role)


def deleteGs(title):
    
    gc = create_client()
    gc.delete(title)

    print('File deleted')
