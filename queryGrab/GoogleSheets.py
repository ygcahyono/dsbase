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
       readGs(file_name, sheet=None, header=True, oauth2 = None)
       you can define the name of sheet using the param `sheet` and choose the header whether it's exist or not
        
        notes on oauth2: 
        - the basic config for the authentification is true so it will use the drive_api2 for the connection in your credentials, 
        - therefore, if you want to make the documents more secure you can pass the oauth2 value with non-None and share the googlesheets document
        with the project mail: data-id-grab@quickstart-1538723811950.iam.gserviceaccount.com. How to? (Go to on the Top Right of document > Share > Enter Email).
        - Param sheet accept integer or string. integer represents the position of worksheet in spreadsheet (1-based). string represent the name of worksheet. if sheet = None, then Sheet1 will be selected
        - Fill null columns. example : df = df.fillna('')
    """

    from pandas import DataFrame
    
    gc = create_client(oauth2)
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

def writeGs(df, file_name, sheet=None, row = 1, col=1, add_worksheet=False, sheet_title=None, oauth2= None):
    """
       writeGs(df, file_name, sheet=None, row = 1, col=1, add_worksheet=False, sheet_title=None, oauth2= None)
       add_worksheet is used when you want to add the new sheet with own name and set the sheet_title with new string.
        
        notes on oauth2: 
        - the basic config for the authentification is true so it will use the drive_api2 for the connection in your credentials, 
        - therefore, if you want to make the documents more secure you can pass the oauth2 value with non-None and share the googlesheets document
        with the project mail: data-id-grab@quickstart-1538723811950.iam.gserviceaccount.com. How to? (Go to on the Top Right of document > Share > Enter Email).
        - Param sheet accept integer or string. integer represents the position of worksheet in spreadsheet (1-based). string represent the name of worksheet. if sheet = None, then Sheet1 will be selected
        - Fill null columns. example : df = df.fillna('')
    """

    gc = create_client(oauth2)
    sh = gc.open(file_name)
    
    if add_worksheet:
        if type(sheet_title)!=type('title') or sheet_title=='':
            raise ValueError('sheet_title must in string form')
        else:
            wks = sh.add_worksheet(sheet_title)
    else:
        wks = find_worksheet(sh,sheet)
    
    wks.clear()
    print('Writing DataFrame...')
    wks.set_dataframe(df,(row,col))
    print('Done writing')

def shareGs(file_name, email_address, role, oauth2= None): 
    """
       shareGs(file_name, email_address, role, oauth2= None)
       is a function for sharing the google sheets document to new email, the role of this function are writer or only reader.
        
        notes on oauth2: 
        - the basic config for the authentification is true so it will use the drive_api2 for the connection in your credentials, 
        - therefore, if you want to make the documents more secure you can pass the oauth2 value with non-None and share the googlesheets document
        with the project mail: data-id-grab@quickstart-1538723811950.iam.gserviceaccount.com. How to? (Go to on the Top Right of document > Share > Enter Email).
        - Param sheet accept integer or string. integer represents the position of worksheet in spreadsheet (1-based). string represent the name of worksheet. if sheet = None, then Sheet1 will be selected
        - Fill null columns. example : df = df.fillna('')
    """

    gc = create_client(oauth2)
    sh = gc.open(file_name)
    roles = ['writer','reader']
    if role not in  roles:
        raise ValueError('role must \'writer\' or \'reader\'\nFile not shared')
        
    sh.share(email_address,role)
    print('Shared')

def createGs(df, file_name, email_address, parent_id = None, role='writer', defined_title= False, worksheet_title= None,oauth2 = None):
    """
       createGs(df, file_name, email_address, parent_id = None, role='writer', defined_title= False, worksheet_title= None,oauth2 = None)
       the value is valued true when you want to create your own sheet name at the first place, and worksheet_title value is string, choose your own.
        
        notes on oauth2: 
        - the basic config for the authentification is true so it will use the drive_api2 for the connection in your credentials, 
        - therefore, if you want to make the documents more secure you can pass the oauth2 value with non-None and share the googlesheets document
        with the project mail: data-id-grab@quickstart-1538723811950.iam.gserviceaccount.com. How to? (Go to on the Top Right of document > Share > Enter Email).
        - Param sheet accept integer or string. integer represents the position of worksheet in spreadsheet (1-based). string represent the name of worksheet. if sheet = None, then Sheet1 will be selected
        - Fill null columns. example : df = df.fillna('')
    """
    gc = create_client(oauth2)
    file_exist = 0
    
    try:
        sh = gc.open(file_name)
        file_exist = 1
    except:
        sh = gc.create(file_name, parent_id)
    
    if file_exist:
        raise ValueError('File already exist. If you want to overwrite the file, use writeGs. If you want to append the DataFrame, use insertGs.')

    if defined_title:
        writeGs(df, file_name, add_worksheet=defined_title, worksheet_title= worksheet_title)
        sh = gc.open(file_name)
        sh.del_worksheet(worksheet = sh.worksheets()[0])
        
    else:
        writeGs(df, file_name)
        
    shareGs(file_name, email_address, role)

def deleteGs(title, oauth2 = None):
    """
       deleteGs(title, oauth2 = None)
       delete the existing google sheet.
        
        notes on oauth2: 
        - the basic config for the authentification is true so it will use the drive_api2 for the connection in your credentials, 
        - therefore, if you want to make the documents more secure you can pass the oauth2 value with non-None and share the googlesheets document
        with the project mail: data-id-grab@quickstart-1538723811950.iam.gserviceaccount.com. How to? (Go to on the Top Right of document > Share > Enter Email).
        - Param sheet accept integer or string. integer represents the position of worksheet in spreadsheet (1-based). string represent the name of worksheet. if sheet = None, then Sheet1 will be selected
        - Fill null columns. example : df = df.fillna('')
    """
    
    gc = create_client(oauth2)
    gc.delete(title)

    print('File deleted')
