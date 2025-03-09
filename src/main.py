from binance.client import Client

import config
from scraper.selenium_scraper import SeleniumScraper
from trading.trader import Trader
from trading.trading_signal_analyzer import TradingSignalAnalyzer

# from scraper.truthbrush_scraper import TruthBrushScraper


def main():
    """
    Entry point of the application.

     This function initializes a SeleniumScraper to fetch latest posts from a configured
     TruthSocial account. For each post, it:
     1. Analyzes the trading signal using TradingSignalAnalyzer
     2. Initializes a Trader instance with Binance API
     3. Retrieves and displays the current price of the detected trading pair
    """
    selenium_scraper = SeleniumScraper(scroll_pause_seconds=config.SCROLL_PAUSE_SEC)
    truthsocial_posts = selenium_scraper.fetch_latest_posts("realDonaldTrump")

    if truthsocial_posts:
        for post in truthsocial_posts:
            post["content"] = (
                "You should invest in BTC for sure guys. It's the future. #BTC #Bitcoin"
            )
            sentiment_analyzer = TradingSignalAnalyzer(post)
            sentiment_analyzer.analyze_signal()

            trader = Trader(
                client=Client(
                    config.BINANCE_API_KEY, config.BINANCE_SECRET_KEY, testnet=True
                ),
                symbol=sentiment_analyzer.trading_pair,
            )
            print(trader.get_price())


if __name__ == "__main__":
    main()
