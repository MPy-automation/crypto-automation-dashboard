def b_chart_maker():    
    import matplotlib.pyplot as plt
    import json
    import os
    from s_program_01_config import CRYPTO_NAMES, DATABASE_PATH, CHART_DIR, BAR_CHART_PATH, BAR_COLORS
    from s_program_04_Logger import get_logger

    logger = get_logger()

    with open(DATABASE_PATH, "r") as f:
        crypto = json.load(f)[0]

    plt.style.use("seaborn-v0_8-darkgrid")
    plt.figure(figsize=(10, 6))
    
    changes = []
    chart_names = [] 

    for i in CRYPTO_NAMES:
        try:
                    changes.append(float(crypto[i]["change"][0].strip("%")))
                    chart_names.append(i)
                    global bars
                    bars = plt.bar(chart_names, changes, color=BAR_COLORS)

                    plt.axhline(0, color="black", linewidth=1)
                    plt.ylabel("Change (%)", fontsize = 12)
                    plt.title("Daily Change", fontsize = 14)

                    
                    for i, v in enumerate(changes):
                        offset = max(changes) * 0.02  
                        if v >= 0:
                            y_pos = v + offset         
                            va = 'bottom'
                        else:
                            y_pos = v - abs(offset)    
                            va = 'top'              
                        plt.text(i, y_pos, f"{v:.2f}%", ha='center', va=va, fontsize=10, fontweight = "bold")

        except (KeyError, IndexError) as e:
            if os.path.exists(BAR_CHART_PATH):
                os.remove(BAR_CHART_PATH)
            logger.warning(f"<Bar_chart> Lack of data to make {i} bar chart")

    try:
        plt.xticks(rotation=90, ha="right")
        plt.legend(bars, chart_names, loc="center left", bbox_to_anchor=(1, 0.5), title="Crypto")
        plt.tight_layout()
        plt.savefig(fr"{CHART_DIR}\bar_chart.png")
        plt.close()
    except:
        pass