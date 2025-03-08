import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from base_scraper import BaseScraper


class SeleniumScraper(BaseScraper):
    """
    Scrapes Truth Social posts using Selenium.
    """

    def __init__(self, scroll_pause_seconds=2):
        self.scroll_pause_seconds = scroll_pause_seconds

    def fetch_latest_posts(self, username):
        """
        Scrapes recent posts from a Truth Social profile using Selenium.

        Uses Selenium to scrape the most recent posts from a Truth Social profile.

        Args:
            username (str): Truth Social username (without @)

        Returns:
            list or None: List of post texts, or None if no posts found/error occurred
        """
        print(f"Selenium scraper: fetching the latest {username} Posts")

        url = f"https://truthsocial.com/@{username}"
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        # circumvent cloudflare blocking
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.6998.45 Safari/537.36"
        )

        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=chrome_options
        )

        try:
            driver.get(url)

            scroll_amount = 200
            time.sleep(self.scroll_pause_seconds)

            # Scroll n times to load more posts
            for i in range(5):
                driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
                time.sleep(self.scroll_pause_seconds)

            # Iterate through each container and get the immediate child with aria-label (The posts text)
            status_elements = driver.find_elements(
                By.CSS_SELECTOR,
                "div[data-testid='status']",  # look for data-testid="status"
            )

            if not status_elements:
                print(
                    "No tweets found. The CSS selectors might have changed or cloudflare is doing blocking."
                )
                return None

            all_tweets = []
            for status in status_elements:
                try:
                    # Get the direct child element that holds the tweet text
                    tweet_elem = status.find_element(By.XPATH, "./div[@aria-label]")
                    tweet_text = tweet_elem.get_attribute("aria-label").strip()
                    if tweet_text:
                        all_tweets.append(tweet_text)
                except Exception as e:
                    # If no direct child with aria-label is found, skip this post
                    print("Error, no aria-label found for this post", e)
                    continue

            return all_tweets if all_tweets else None

        except Exception as e:
            print("Error:", e)
            return None
        finally:
            driver.quit()
