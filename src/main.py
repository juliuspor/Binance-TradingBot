from binance.client import Client

import config
from repository.post_repository import PostRepository
from scraper.selenium_scraper import SeleniumScraper
from trading.trader import Trader
from trading.trading_signal_analyzer import TradingSignalAnalyzer

# from scraper.truthbrush_scraper import TruthBrushScraper


def main():
    """
    Entry point of the application.

     Initializes a SeleniumScraper to fetch latest posts from Donald Trump. For each post, it:
     1. Checks if the post has been processed before
     2. Analyzes the trading signal using TradingSignalAnalyzer for new posts
     3. Initializes a Trader instance with Binance API
     4. Displays the current price of the detected trading pair
     5. Places a buy order for a small quantity
     6. Marks the post as processed
    """
    # Initialize SeleniumScraper to scrape latest posts
    selenium_scraper = SeleniumScraper(scroll_pause_seconds=config.SCROLL_PAUSE_SEC)
    truthsocial_posts = selenium_scraper.fetch_latest_posts("realDonaldTrump")

    # Post repository to persist posts
    post_repository = PostRepository()

    if truthsocial_posts:
        latest_post = truthsocial_posts[0]  # latest post

        # Check if this post has already been processed
        if post_repository.is_post_processed(latest_post):
            print(f"Post already processed. Skipping: {latest_post['content']}...")
            return

        # Process the new post
        sentiment_analyzer = TradingSignalAnalyzer(latest_post)
        sentiment_analyzer.analyze_signal()

        try:
            trader = Trader(
                client=Client(
                    config.BINANCE_API_KEY, config.BINANCE_SECRET_KEY, testnet=True
                ),
                symbol=sentiment_analyzer.trading_pair,
            )
            if (
                sentiment_analyzer.trade_signal != "LONG"
                and sentiment_analyzer.trade_signal != "SHORT"
            ):
                print(
                    "No crypto trading relevance detected, skipping this TruthSocial Post."
                )
                return

            print(trader.get_price())
            if sentiment_analyzer.trade_signal == "LONG":
                print(trader.place_buy_order(0.001))
            elif sentiment_analyzer.trade_signal == "SHORT":
                print("Short signal detected. Skipping order placement.")
        except Exception as e:
            print("Error placing order: ", e)
        finally:
            # Mark the post as processed
            post_repository.mark_post_as_processed(latest_post)


if __name__ == "__main__":
    main()
