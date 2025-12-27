def get_logger():
    import logging
    from pathlib import Path
    from s_program_01_config import LOG_DIR, LOG_FILE_NAME

    log_dir = Path(LOG_DIR)
    log_dir.mkdir(exist_ok=True)

    log_file = fr"{log_dir}/{LOG_FILE_NAME}"

    logger = logging.getLogger("retry")
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(
            logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
        )
        logger.addHandler(file_handler)

    return logger
