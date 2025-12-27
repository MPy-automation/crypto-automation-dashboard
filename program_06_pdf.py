def pdf_maker():
    ### Import necessary libraries ###
    from reportlab.lib.pagesizes import A4, A5
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib import colors
    from reportlab.lib.utils import ImageReader
    from reportlab.lib.units import inch
    from PyPDF2 import PdfMerger
    from datetime import datetime
    import json
    import os, shutil
    from s_program_01_config import DATABASE_PATH, CRYPTO_NAMES, CHART_DIR, PDF_DIR, BAR_CHART_PATH
    from s_program_04_Logger import get_logger

    def basic_page(): ### Generate the introduction page ###
        if not os.path.exists(PDF_DIR): ### Verify that the PDF output directory exists ###
            os.makedirs(PDF_DIR)
        else: ### Clear directory ###
            shutil.rmtree(PDF_DIR)
            os.makedirs(PDF_DIR)

        doc = SimpleDocTemplate(fr"{PDF_DIR}\Basic View PDF.pdf", pagesize=A4)
        styles = getSampleStyleSheet()
        elements = []


        ### Set PDF document title ###
        elements.append(Paragraph("📈 <b>Regular crypto report</b>", styles["Title"]))
        elements.append(Spacer(1, 20))
        elements.append(Paragraph(f"Creation date: {datetime.now()}", styles["Normal"]))
        elements.append(Spacer(1, 50))
        
        
        ### Add table to the PDF document ###
        data = [ 
            ["Crypto", "Price (USD)", "Change (%)"], ### Define table header ###
        ]


        ### Populate table with data ###
        for i in CRYPTO_NAMES:
            try:
                data.append([i, crypto[i]["values"][-1], crypto[i]["change"][0]])
            except (KeyError, IndexError): ### Handle missing or empty data ###
                logger.warning(f"<PDF> Lack of data to make a full table {i}")
                try:
                    data.append([i, crypto[i]["values"][-1]])
                except (KeyError, IndexError): ### Handle missing or empty data ###
                    pass


        ### Apply styling to the table ###
        table = Table(data)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("ALIGN", (1, 1), (-1, -1), "CENTER")
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 100))


        ### Add bar chart if available ###
        if os.path.exists(BAR_CHART_PATH):
            elements.append(Image(BAR_CHART_PATH, width=600, height=300))
            elements.append(Spacer(1, 20))

        doc.build(elements)


    def each_crypto(): ### Create a page for each cryptocurrency ###
        merger = PdfMerger()
        merger.append(fr"{PDF_DIR}\Basic View PDF.pdf")

        for i in CRYPTO_NAMES: ### For each cryptocurrency ###
            try:
                crypto_doc_1 = SimpleDocTemplate(fr"{PDF_DIR}\{i}.pdf", pagesize=A5)
                styles = getSampleStyleSheet()
                
                elements = []
                elements.append(Paragraph(i, styles["Title"]))
                elements.append(Spacer(1, 20))

                try:
                    elements.append(Paragraph(f'Price: {crypto[i]["values"][0]}$', styles["Normal"]))
                except KeyError: ### Handle missing values ###
                    logger.warning(f"<PDF> Lack of data to make a title")
                elements.append(Spacer(1, 20))


                ### Automatically adjust image ###
                img_path = f"{CHART_DIR}\{i}_chart.png"

                if not os.path.exists(img_path):
                    raise ValueError
                
                page_width, page_height = A5
                
                max_width = page_width - 0.6 * inch  ### Margin ### 
                max_height = page_height - 3 * inch  ### Space for text ###

                img_reader = ImageReader(img_path) ### Load the Image ###
                orig_w, orig_h = img_reader.getSize()

                ### Maintain aspect ratio ###
                ratio = orig_h / orig_w

                ### Fit image to page width ###
                new_w = max_width
                new_h = new_w * ratio

                ### Handle case when image is too tall for the page ###
                if new_h > max_height:
                    new_h = max_height
                    new_w = new_h / ratio

                elements.append(Image(img_path, width=new_w, height=new_h))
                ### End automatic image adjustment ###
                
                crypto_doc_1.build(elements)
                merger.append(fr"{PDF_DIR}\{i}.pdf") ### Add page to PDF ###

            except ValueError: ### Handle error when cryptocurrency data is missing ###
                logger.warning(f"<PDF> Couldn't create {i} pdf page ({i} chart doesn't exist)")

        merger.write(fr"{PDF_DIR}\Merged PDF.pdf")
        merger.close()

    with open(DATABASE_PATH, "r") as f: ### Load data from database ###
        crypto = json.load(f)[0]

    logger = get_logger()

    ### Call functions to generate the PDF ###
    basic_page()
    each_crypto()