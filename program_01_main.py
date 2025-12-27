import os
from program_02_request import get_data
from program_03_spreadsheet import insert_data
from program_04_line_chart import l_chart_maker
from program_05_bar_chart import b_chart_maker
from program_06_pdf import pdf_maker
from program_07_task_scheduler import set_schedule
from s_program_01_config import LOG_DIR, LOG_FILE_NAME
from s_program_03_Acces_Token import new_token
from s_program_04_Logger import get_logger

def main():
    try:
        crypto_name, price, date = get_data()
        logger.info("<Request> Completed successfully")
    except:
        logger.error("Unexpected Error in program_02_request")
        return False
    
    try:
        insert_data(crypto_name, price, date)
        logger.info("<Spreadsheet> Completed successfully")
    except Exception as e:
        if str(e) == "('invalid_grant: Bad Request', {'error': 'invalid_grant', 'error_description': 'Bad Request'})" or str(e) == "[Errno 2] No such file or directory: 'J_token.json'": 
            logger.warning("<Spreadsheet> Expired Token")
            logger.warning("<Spreadsheet> Wait please")
            new_token()
            insert_data(crypto_name, price, date)
        else:
            logger.error(f"Unexpected Error in program_03_spreadsheet {e}")
        return False

    try:
        l_chart_maker()
        logger.info("<Line_chart> Completed successfully")
    except:
        logger.error("Unexpected Error in program_04_line_chart")
        return False
    
    try:
        b_chart_maker()
        logger.info("<Bar_chart> Completed successfully")
    except:
        logger.error("Unexpected Error in program_05_bar_chart")
        return False
    
    try:
        pdf_maker()
        logger.info("<PDF> Completed successfully")
    except:
        logger.error("Unexpected Error in program_06_pdf")
        return False
    
    try:
        set_schedule()
        logger.info("<Task_scheduler> Completed successfully")
        return True
    except:
        logger.error(f"Unexpected Error in program_07_task_scheduler")
        return False
    
if os.path.exists(fr"{LOG_DIR}\{LOG_FILE_NAME}"):
    os.remove(fr"{LOG_DIR}\{LOG_FILE_NAME}")

logger = get_logger()

try:
    if __name__ == "__main__":
        if main():
            logger.info(f'Success!')
except:
    logger.error(f"Unexpected Error in program_01_main") 