### Settings ###

# Path to Python executable – replace with your own path
PYTHON_PATH = "C:/Path/To/Python/python.exe"

# Path to main script – replace with your own path
SCRIPT_PATH = "C:/Path/To/Project/main.py"



CLIENT_SECRET_PATH = "j_client_secret.json"
TOKEN_PATH = "j_token.json"
CRYPTO_URLS = [
    f"https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT",
    f"https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT",
    f"https://api.binance.com/api/v3/ticker/price?symbol=ADAUSDT",
    f"https://api.binance.com/api/v3/ticker/price?symbol=SOLUSDT",
    f"https://api.binance.com/api/v3/ticker/price?symbol=DOGEUSDT", 
]
FILE_NAME = "Crypto Overview"
SHEET_NAME = "Crypto Price"
CRYPTO_NAMES = ['BTCUSDT', 'ETHUSDT', 'ADAUSDT', 'SOLUSDT', 'DOGEUSDT']
CRYPTO_NAMES.sort() # Alphabetically
COUNT_EACH_VALUES = 5 # How many prices we want to the chart to each crypto (if they're available from spreadsheet table)
DATABASE_PATH = "j_crypto_database.json" 
ID_PATH = "spreadsheet.txt"
SHEET_ID_PATH = "sheet_id.txt"
CHART_DIR = "charts"
PDF_DIR = "pdf"
BAR_CHART_PATH = fr"{CHART_DIR}\bar_chart.png"
BAR_COLORS = ["orange", "blue", "green", "purple", "red"]
LOG_DIR = "logs"
LOG_FILE_NAME = "info.log"
