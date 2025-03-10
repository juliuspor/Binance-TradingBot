import time

import schedule

from trading_bot import TradingBot


def job():
    bot = TradingBot()
    bot.run()


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
    # Run immediately once
    job()

    # Then schedule to run every n seconds
    schedule.every(60).seconds.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
