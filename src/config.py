import os

from dotenv import load_dotenv

load_dotenv()

BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_SECRET_KEY = os.getenv("BINANCE_SECRET_KEY")
TRUTHSOCIAL_USERNAME = os.getenv("TRUTHSOCIAL_USERNAME")
TRUTHSOCIAL_PASSWORD = os.getenv("TRUTHSOCIAL_PASSWORD")

SCROLL_PAUSE_SEC = 3

SYMBOL = "BTCUSDT"


if not BINANCE_API_KEY or not BINANCE_SECRET_KEY:
    raise ValueError("API Key or Secret Key is missing")
