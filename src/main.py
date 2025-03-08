"""
Binance Trading Bot entry point to automate trading decisions based on trump truth social posts.
"""

import json

from binance.client import Client

import config
from bot.trader import get_price, place_buy_order
from selenium_scraper import SeleniumScraper
from truthbrush_scraper import TruthBrushScraper

client = Client(config.BINANCE_API_KEY, config.BINANCE_SECRET_KEY, testnet=True)

print(get_price(client, config.SYMBOL))
print(place_buy_order(client, config.SYMBOL, 0.001))

seleniumScraper = SeleniumScraper()

selenium_tweets = seleniumScraper.fetch_latest_posts(config.USERNAME)

if selenium_tweets:
    try:
        with open("tweets.json", "w", encoding="utf-8") as f:
            json.dump(selenium_tweets, f, indent=4, ensure_ascii=False)
        print(f"Saved {len(selenium_tweets)} tweets to {"tweets.json"}")
    except IOError as e:
        print("Error writing to file:", e)
else:
    print("No tweets fetched. Nothing to save.")
