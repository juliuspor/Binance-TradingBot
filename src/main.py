import json

from binance.client import Client

import config
from bot.trader import Trader
from bot.trading_signal_analyzer import TradingSignalAnalyzer
from scraper.selenium_scraper import SeleniumScraper

# from scraper.truthbrush_scraper import TruthBrushScraper


def main():
    """
    Entry point of the application.

    This function initializes a Trader instance with the Binance API client,
    fetches the current price of the configured symbol (eg. ETH/USDT), initializes a SeleniumScraper,
    and uses it to fetch latest posts from a TruthSocial account.
    The fetched tweets are then saved to a JSON file.

    """
    trader = Trader(
        client=Client(config.BINANCE_API_KEY, config.BINANCE_SECRET_KEY, testnet=True),
        symbol=config.SYMBOL,
    )

    print(trader.get_price())

    selenium_scraper = SeleniumScraper(scroll_pause_seconds=config.SCROLL_PAUSE_SEC)

    selenium_posts = selenium_scraper.fetch_latest_posts(config.USERNAME)

    if selenium_posts:
        for post in selenium_posts:
            sentiment_analyzer = TradingSignalAnalyzer(post)
            sentiment_analyzer.analyze_signal()
            print(sentiment_analyzer.result)

    if selenium_posts:
        try:
            with open("tweets.json", "w", encoding="utf-8") as f:
                json.dump(selenium_posts, f, ensure_ascii=False, indent=4)
            print(f"Saved {len(selenium_posts)} tweets to tweets.json")
        except IOError as e:
            print("Error writing to file:", e)
    else:
        print("No tweets fetched. Nothing to save.")


if __name__ == "__main__":
    main()
