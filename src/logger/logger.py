import logging
import os
from dotenv import load_dotenv

load_dotenv(verbose=True)

# 環境変数からログレベルを取得し、デフォルトをINFOに設定
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()


def setup_logger():
    logger = logging.getLogger("smart_home_logger")
    logger.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))

    # ハンドラが既に設定されていないか確認
    if not logger.hasHandlers():
        # コンソールハンドラ
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # フォーマッター
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        ch.setFormatter(formatter)

        # ハンドラをロガーに追加
        logger.addHandler(ch)

    logger.info(f"Logger is set up with log level {LOG_LEVEL}")

    return logger


logger = setup_logger()
