"""
Binance Trading Bot entry point to automate trading decisions based on trump truth social posts.
"""

from binance.client import Client

import config
from bot.trader import get_price, place_buy_order
from scraper import fetch__n_latest_posts

client = Client(config.BINANCE_API_KEY, config.BINANCE_SECRET_KEY, testnet=True)

print(get_price(client, config.SYMBOL))
print(place_buy_order(client, config.SYMBOL, 0.001))

latest_posts = fetch__n_latest_posts("realDonaldTrump", 4)
for latest_post in latest_posts:
    latest_post_text = latest_post.get("content", "").strip()
    print(latest_post_text)
