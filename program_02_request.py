def get_data():
    import requests
    from datetime import datetime
    from s_program_01_config import CRYPTO_URLS
    from s_program_02_utils import get_decimals

    symbols = []
    prices = []
    dates = []

    for i in CRYPTO_URLS:
        response = requests.get(i)

        if response.status_code == 200: 
            data = response.json() 
            symbols.append(data["symbol"])
            prices.append(round(float(data["price"]), get_decimals(float(data["price"]))))
            dates.append(datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))
        else:
            raise ValueError

    return symbols, prices, dates
