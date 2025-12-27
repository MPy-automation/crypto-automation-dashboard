from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from s_program_01_config import TOKEN_PATH

def credentials(): ### Function for setting up technical components required to connect to the file ###
    creds = Credentials.from_authorized_user_file(TOKEN_PATH)

    if creds.expired and creds.refresh_token: ### Refresh token ###
        creds.refresh(Request())
    
        with open(TOKEN_PATH, "w") as token_file: ### Save ###
            token_file.write(creds.to_json())

    global service_v3, service_v4
    service_v3 = build("drive", "v3", credentials=creds)
    service_v4 = build("sheets", "v4", credentials=creds)
    
    return service_v3, service_v4

def get_decimals(price): ### Rounding function ###
    price = abs(price)
    
    if price >= 1000:
        return 3
    elif price >= 100:
        return 4
    elif price >= 0.01:
        return 5
    elif price >= 0.0001:
        return 7
    else:
        return 8
    
def set_style(spreadsheet_id, sheet_id, background_color): ### Function for styling cells ###
    service_v4.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={
            "requests": [
                {
                    "repeatCell": {
                        "range": {
                            "sheetId": sheet_id,
                            "startRowIndex": 0,
                            "endRowIndex": 1,
                            "startColumnIndex": 0,
                            "endColumnIndex": 4
                        },
                        "cell": {
                            "userEnteredFormat": {
                                "backgroundColor": background_color,
                                "horizontalAlignment": "CENTER",
                                "textFormat": {
                                    "foregroundColor": {"red": 1, "green": 1, "blue": 1},
                                    "bold": True
                                }
                            }
                        },
                        "fields": "userEnteredFormat(backgroundColor, textFormat, horizontalAlignment)"
                        }
                    }, 

                {
                    "updateDimensionProperties": {
                    "range": {
                        "sheetId": sheet_id,
                        "dimension": "COLUMNS",
                        "startIndex": 2,   
                        "endIndex": 3     
                    },
                    "properties": {
                        "pixelSize": 140
                    },
                    "fields": "pixelSize"
                    }
                },
                ]
            }
        ).execute()



    
