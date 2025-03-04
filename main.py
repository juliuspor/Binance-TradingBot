import os

from binance.client import Client
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_SECRET_KEY")

if not API_KEY or not API_SECRET:
    raise ValueError("API Key or Secret Key is missing")

client = Client(API_KEY, API_SECRET, testnet=True)

# print(client.get_account())

symbol = "BTCUSDT"


def get_price():
    return float(client.get_symbol_ticker(symbol=symbol)["price"])


def place_buy_order(symbol, quantity):
    order = client.order_market_buy(symbol=symbol, quantity=0.001)
    print("buy order done: ", order)


print(get_price())
print(place_buy_order(symbol, 0.001))
