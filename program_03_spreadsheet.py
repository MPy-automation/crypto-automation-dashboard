def insert_data(crypto_names, prices, dates):    
    
    ### Import necessary libraries ###
    import json
    import os
    from s_program_01_config import FILE_NAME, SHEET_NAME, CRYPTO_NAMES, ID_PATH, DATABASE_PATH, COUNT_EACH_VALUES, SHEET_ID_PATH
    from s_program_02_utils import get_decimals, credentials, set_style
    from s_program_04_Logger import get_logger
    service_v3, service_v4 = credentials()

    def create_file(): ### Function to create file if it doesn't exist ###
        ### Create file ###
        sheet_metadata = {
            "name": FILE_NAME,
            "mimeType": "application/vnd.google-apps.spreadsheet"
        }

        sheet_file = service_v3.files().create(
            body=sheet_metadata,
            fields="id, name"
        ).execute()


        ### Rename sheet ###
        spreadsheet = service_v4.spreadsheets().get(
            spreadsheetId=sheet_file["id"]
        ).execute()

        sheets = spreadsheet.get("sheets", [])

        for sheet in sheets:
            sheet_id = sheet["properties"]["sheetId"]  ### Numeric ID of the sheet ###

        request_body = {
            "requests": [
                {
                    "updateSheetProperties": {
                        "properties": {
                            "sheetId": sheet_id,
                            "title": f"{SHEET_NAME}"
                        },
                        "fields": "title"
                    }

                }
            ]
        }

        service_v4.spreadsheets().batchUpdate(
            spreadsheetId=sheet_file["id"],
            body=request_body
        ).execute()

        with open(ID_PATH, "w") as f: ### Write file ID to a text file ###
            f.write(sheet_file["id"])
        
        with open(SHEET_ID_PATH, "w") as f: ### Write sheet ID to a text file ###
            f.write(str(sheet_id))


        ### Write table header ###
        values = [
            ["Crypto Name", "Price", "Date", "Change %"]
        ]

        body = {"values": values}

        service_v4.spreadsheets().values().update(
            spreadsheetId=sheet_file["id"],
            range=f"{SHEET_NAME}!A1:D1",  
            valueInputOption="RAW",  
            body=body
        ).execute()


        ### Call function to style cells ###
        set_style(sheet_file["id"], sheet_id, {"red": 0.2, "green": 0.6, "blue": 1})

    def verify(): ### Function to verify file existence ###
        query = "'root' in parents and trashed=false" 
        results = service_v3.files().list(
            q=query,
            spaces='drive',
            fields="files(id, name)",
            pageSize=100
        ).execute()

        folders = results.get('files', [])

        exist = False

        for folder in folders:
            if folder["name"] == FILE_NAME:
                exist = True
                break

        if not exist: ### Verify if the file exists ###
            create_file() ### Call function to create the file ###
            
            if os.path.exists(DATABASE_PATH):
                os.remove(DATABASE_PATH)
        return exist
    
    def get_previous_values(): ### Function to retrieve previous values ###
        result = service_v4.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=f"{SHEET_NAME}!A:D" 
        ).execute()
            
        values = result.get("values", [])[-(len(CRYPTO_NAMES)*COUNT_EACH_VALUES*2):]
        global values_count
        values_count = len(result.get("values", [])) 

        crypto_dict = {}
        
        for i in CRYPTO_NAMES:
            crypto_dict[i] = {
                 "values": [], 
                 "dates": [], 
                 "change": []
            }

        for i in range(1, len(values)):
             if not any(len(crypto_dict[crypto]["values"]) < COUNT_EACH_VALUES for crypto in CRYPTO_NAMES):
                break
             
             if (len(crypto_dict[values[i][0]]["values"])) < COUNT_EACH_VALUES:
                  prices = crypto_dict[values[i][0]]["values"] 
                  dates = crypto_dict[values[i][0]]["dates"] 

                  prices.append(values[i][1])
                  dates.append(values[i][2])

                  crypto_dict[values[i][0]]["values"] = prices
                  crypto_dict[values[i][0]]["dates"] = dates

        with open(DATABASE_PATH, "w") as f: ### Write values to a database ###
            json.dump([crypto_dict], f)

    def append_row(spreadsheet_id, previous_values): ### Function to add data to the file ###
        values_append = []
        percentages = []
        
        with open(DATABASE_PATH, "r") as f: ### Load values from the database ###
            crypto = json.load(f)

        ### Modify data for each cryptocurrency ###
        for i in range(len(crypto_names)):
            try:
                if previous_values[crypto_names[i]][0]:                        
                            if "," in previous_values[crypto_names[i]][0]:
                                previous_price_list = (previous_values[crypto_names[i]][0]).split(",")
                                previous_price = float(previous_price_list[0] + "." + previous_price_list[1])
                            else:
                                previous_price = float(previous_values[crypto_names[i]][0].split("$")[1])

                            percentage = (prices[i]-previous_price)*100/previous_price
                            percentage = str(round(percentage, get_decimals(percentage)))

                            if float(percentage) >= 0:  
                                percentage = "+" + percentage

                            values_append.append([crypto_names[i], "$" + str(prices[i]), dates[i], percentage + "%"])
                            percentages.append(percentage) 

                            crypto[0][crypto_names[i]]["change"] = [percentage] 
            except: ### Handle error if data is insufficient ###
                logger.warning(f"<Spreadsheet> Missing values to make procentual change of {crypto_names[i]}")
                values_append.append([crypto_names[i], "$" + str(prices[i]), dates[i]])
                
            values = crypto[0][crypto_names[i]]["values"]
            values.append("$" + str(prices[i]))
            
            while len(values) > COUNT_EACH_VALUES: ### Ensure only the set number of values remain in the database ###
                values.pop(0)
            crypto[0][crypto_names[i]]["values"] = values

            
            dates_ = crypto[0][crypto_names[i]]["dates"]
            dates_.append(dates[i])

            while len(dates_) > COUNT_EACH_VALUES: ### Ensure only the set number of values remain in the database ###
                dates_.pop(0)
            crypto[0][crypto_names[i]]["dates"] = dates_
            
            

        with open(DATABASE_PATH, "w") as f: ### Write modified information back to the database ###
            json.dump(crypto, f)

        body_append = {"values": values_append}

        service_v4.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            range=SHEET_NAME,  
            valueInputOption="RAW", 
            insertDataOption="INSERT_ROWS", 
            body=body_append
        ).execute()


        ### Conditional formatting for the "change" column ###
        with open(SHEET_ID_PATH, "r") as f:
            sheet_file_id = f.read()
                
        service_v4.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={
            "requests": [

            ### Green - if text contains "+" ###
            {
                "addConditionalFormatRule": {
                "rule": {
                    "ranges": [
                        {
                            "sheetId": sheet_file_id,           
                            "startRowIndex": values_count,                     
                            "startColumnIndex": 0,        
                            "endColumnIndex": 4         
                        }
                    ],
                    "booleanRule": {                 
                        "condition": {
                            "type": "TEXT_STARTS_WITH",  
                            "values": [{"userEnteredValue": "+"}]
                        },
                        "format": {                    
                            "backgroundColor": {"red": 0, "green": 1, "blue": 0},
                            "textFormat": {"bold": True, "foregroundColor": {"red": 0, "green": 0, "blue": 0}}
                        }
                    }
                },
                "index": 0                           
            }
        },


            ### Red - if text contains "-" ###
            {
                "addConditionalFormatRule": {
                    "rule": {
                        "ranges": [{
                            "sheetId": sheet_file_id,
                            "startRowIndex": values_count,
                            "startColumnIndex": 3,
                            "endColumnIndex": 4
                        }],
                        "booleanRule": {
                            "condition": {
                                "type": "TEXT_STARTS_WITH",
                                "values": [{"userEnteredValue": "-"}]
                            },
                            "format": {
                                "backgroundColor": {"red": 1, "green": 0, "blue": 0},
                                "textFormat": {"bold": True, "foregroundColor": {"red": 1, "green": 1, "blue": 1}}
                            }
                        }
                    },
                    "index": 1
                }
            }

        ]
    }
).execute()

    logger = get_logger()
    exist = verify() ### Call function to verify and save status ###
    
    ### Create Database if not exists ###
    if not os.path.exists(DATABASE_PATH):
        json_crypto = {}

        for i in CRYPTO_NAMES:
            json_crypto[i] = {"values": [], "change": [], "dates": []}

        with open(DATABASE_PATH, "w") as f:
            json.dump([json_crypto], f)

    with open(ID_PATH, "r") as f: ### Write file ID to text file ###
         spreadsheet_id = f.read()

    with open(SHEET_ID_PATH, "r") as f: ### Write sheet ID to text file ###
         sheet_id = f.read()

    if exist:
        get_previous_values() ### Call function to get previous values ### 
        
        with open(DATABASE_PATH, "r") as f: ### Load data from the database ###
            crypto = json.load(f)[0]
        
        previous_values = {}
        
        for i in CRYPTO_NAMES:
            try:
                previous_values[i] = [crypto[i]["values"][-1]]
            except IndexError: ### Handle error if information is missing ###
                logger.warning("<Spreadsheet> Lack of previous data")
        append_row(spreadsheet_id, previous_values) ### Call function to add data ###
    else:
        previous_values = {}
        global values_count
        values_count = 1
        append_row(spreadsheet_id, previous_values) ### Call function to add data ###
        set_style(spreadsheet_id, sheet_id, {"red": 1.0, "green": 0.647, "blue": 0.0}) ### Apply cell styling ###
    



