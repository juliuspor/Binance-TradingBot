import json

from binance.client import Client

import config
from bot.trader import Trader
from scraper.selenium_scraper import SeleniumScraper
from scraper.truthbrush_scraper import TruthBrushScraper


def main():
    """
    Entry point of the application.

    This function initializes a Trader instance with the Binance API client,
    fetches the current price of the configured symbol, initializes a SeleniumScraper,
    and uses it to fetch latest posts from a configured Twitter/X username.
    The fetched tweets are then saved to a JSON file.

    Returns:
        None
    """
    trader = Trader(
        client=Client(config.BINANCE_API_KEY, config.BINANCE_SECRET_KEY, testnet=True),
        symbol=config.SYMBOL,
    )

    print(trader.get_price())

    seleniumScraper = SeleniumScraper(scroll_pause_seconds=config.SCROLL_PAUSE_SEC)

    selenium_tweets = seleniumScraper.fetch_latest_posts(config.USERNAME)

    if selenium_tweets:
        try:
            with open("tweets.json", "w", encoding="utf-8") as f:
                json.dump(selenium_tweets, f, indent=4, ensure_ascii=False)
            print(f"Saved {len(selenium_tweets)} tweets to tweets.json")
        except IOError as e:
            print("Error writing to file:", e)
    else:
        print("No tweets fetched. Nothing to save.")


if __name__ == "__main__":
    main()
