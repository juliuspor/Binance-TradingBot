from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException

import config
from repository.post_repository import PostRepository
from scraper.selenium_scraper import SeleniumScraper
from trading.trader import Trader
from trading.trading_signal_analyzer import TradingSignalAnalyzer


class TradingBot:
    """Bot that scrapes posts, analyzes them for trading signals, and executes trades."""

    def __init__(self):
        """Initialize scraper and repository components."""
        self.selenium_scraper = SeleniumScraper()
        self.post_repository = PostRepository()

    def fetch_latest_post(self):
        """Fetch the most recent post from the configured user.

        Returns:
            dict: Latest post data or None if no posts found
        """
        truthsocial_posts = self.selenium_scraper.fetch_latest_posts(
            config.USERNAME_TO_SCRAPE
        )
        if truthsocial_posts:
            return truthsocial_posts[0]
        return None

    def process_latest_post(self, post):
        """Analyze post for trading signals and execute trades if applicable.

        Args:
            post (dict): Post data to analyze and process
        """
        if self.post_repository.is_post_processed(post):
            print(f"Post already processed. Skipping: {post['content'][:60]}, {"..."}")
            return
        sentiment_analyzer = TradingSignalAnalyzer(post)
        sentiment_analyzer.analyze_signal()
        try:
            trader = Trader(
                client=Client(
                    config.BINANCE_API_KEY, config.BINANCE_SECRET_KEY, testnet=True
                ),
                symbol=sentiment_analyzer.trading_pair,
            )
            if sentiment_analyzer.trade_signal not in ["LONG", "SHORT"]:
                print(
                    f"No crypto relevance detected. Skipping: {post['content'][:60]}, {"..."}"
                )
                return

            if sentiment_analyzer.trade_signal == "LONG":
                trader.place_buy_order(0.01)
            elif sentiment_analyzer.trade_signal == "SHORT":
                trader.place_sell_order(0.01)
        except (BinanceAPIException, BinanceOrderException) as e:
            print(f"Error executing trade: {e}")
        except ConnectionError as e:
            print(f"Connection error during trade execution: {e}")
        except ValueError as e:
            print(f"Value error in trade parameters: {e}")
            print(f"Error executing trade: {e}")
        finally:
            self.post_repository.mark_post_as_processed(post)

    def run(self):
        """Execute the main bot workflow: fetch post, process it."""
        latest_post = self.fetch_latest_post()
        if latest_post:
            self.process_latest_post(latest_post)
