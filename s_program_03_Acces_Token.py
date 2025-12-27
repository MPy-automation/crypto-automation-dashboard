def new_token():
    from google_auth_oauthlib.flow import InstalledAppFlow
    from s_program_01_config import CLIENT_SECRET_PATH, TOKEN_PATH

    SCOPES = [
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/spreadsheets"
    ]

    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_PATH, SCOPES)

    creds = flow.run_local_server(
        port=0,
        prompt='consent',          
    )

    ### Save Token ###
    with open(TOKEN_PATH, "w") as token_file:
        token_file.write(creds.to_json())

