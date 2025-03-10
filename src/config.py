import os

from dotenv import load_dotenv

load_dotenv()

BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_SECRET_KEY = os.getenv("BINANCE_SECRET_KEY")
TRUTHSOCIAL_USERNAME = os.getenv("TRUTHSOCIAL_USERNAME")
TRUTHSOCIAL_PASSWORD = os.getenv("TRUTHSOCIAL_PASSWORD")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

USERNAME_TO_SCRAPE = "realDonaldTrump"
SCROLL_PAUSE_SEC = 3

if not BINANCE_API_KEY or not BINANCE_SECRET_KEY:
    raise ValueError("Binance API Key or Binance Secret Key is missing")
