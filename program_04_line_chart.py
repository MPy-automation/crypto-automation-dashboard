def l_chart_maker():    
    import matplotlib.pyplot as plt
    import json
    import os
    from s_program_01_config import CRYPTO_NAMES, DATABASE_PATH, CHART_DIR
    from s_program_04_Logger import get_logger

    def make_chart():
        with open(DATABASE_PATH, "r") as f:
            crypto = json.load(f)[0]

        for i in CRYPTO_NAMES:
            try:        
                dny = (crypto[i]["dates"])
                ceny = list(map(lambda x: float(x.strip("$")), (crypto[i]["values"])))
                
                if len(ceny) < 2:
                    raise KeyError

                plt.style.use("seaborn-v0_8-darkgrid")
                plt.xticks(rotation=90, ha='center')
                plt.plot(dny, ceny, marker="o", color="blue", linewidth=2)
                plt.title(f"{i} Price Chart")
                plt.ylabel("Price in USD")
                plt.grid(True)
                
                plt.tight_layout(pad=1.5)
                plt.savefig(f"{CHART_DIR}\{i}_chart.png", dpi=300) 
                plt.close()
            except KeyError:
                logger.warning(f"<Line_chart> Lack of data to make {i} line chart")
                
                if os.path.exists(fr"{CHART_DIR}\{i}_chart.png"):
                    os.remove(fr"{CHART_DIR}\{i}_chart.png")

    if not os.path.exists(CHART_DIR):
        os.makedirs(CHART_DIR)

    logger = get_logger()
    make_chart()