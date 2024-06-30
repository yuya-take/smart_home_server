import logging
import os


from dotenv import load_dotenv

load_dotenv(verbose=True)

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


def setup_logger():
    logger = logging.getLogger("smart_home_logger")
    logger.setLevel(LOG_LEVEL)

    # コンソールハンドラ
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # フォーマッター
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ch.setFormatter(formatter)

    # ハンドラをロガーに追加
    if not logger.hasHandlers():
        logger.addHandler(ch)

    logger.info(f"Logger is set up with log level {LOG_LEVEL}")

    return logger


logger = setup_logger()
