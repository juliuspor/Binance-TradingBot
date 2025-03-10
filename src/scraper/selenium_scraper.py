import hashlib
import os
import platform
import time

from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from scraper.base_scraper import BaseScraper  # pylint: disable=import-error


class SeleniumScraper(BaseScraper):
    """
    Scrapes Truth Social posts using Selenium.
    """

    def __init__(self, scroll_pause_seconds=2):
        self.scroll_pause_seconds = scroll_pause_seconds

    def _is_running_in_docker(self):
        """Check if the code is running inside a Docker container."""
        # Check for .dockerenv file
        return os.path.exists("/.dockerenv") or os.environ.get("DOCKER_CONTAINER")

    def fetch_latest_posts(self, username):
        """
        Scrapes recent posts from a Truth Social profile using Selenium.

        Uses Selenium to scrape the most recent posts from a Truth Social profile.

        Args:
            username (str): Truth Social username (without @)

        Returns:
            list or None: List of post texts, or None if no posts found/error occurred
        """
        print(f"Selenium scraper: fetching the latest {username} TruthSocial Posts")

        # Configure ChromeDriver for both Docker and local environments
        url = f"https://truthsocial.com/@{username}"
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")  # Required in Docker
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-dev-shm-usage")  # Required in Docker
        # circumvent cloudflare blocking
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.6998.45 Safari/537.36"
        )

        # Debug information
        is_docker = self._is_running_in_docker()
        print(f"Running in Docker: {is_docker}")

        if is_docker:
            # In Docker: use the system chromedriver directly without WebDriverManager
            print("Using system ChromeDriver in Docker")
            # Check if chromedriver exists at the expected path
            chromedriver_path = "/usr/bin/chromedriver"
            if os.path.exists(chromedriver_path):
                print(f"ChromeDriver found at {chromedriver_path}")
            else:
                print(f"Warning: ChromeDriver not found at {chromedriver_path}")
                # Try alternative location
                chromedriver_path = "/usr/lib/chromium/chromedriver"
                print(f"Trying alternative path: {chromedriver_path}")

            service = Service(executable_path=chromedriver_path)
            chrome_options.binary_location = "/usr/bin/chromium"
        else:
            # On local machine: use WebDriverManager
            print("Using WebDriverManager for local development")
            service = Service(ChromeDriverManager().install())

        try:
            # Create the driver with appropriate options
            driver = webdriver.Chrome(service=service, options=chrome_options)

            # Continue with the rest of your scraping code...
            driver.get(url)

            scroll_amount = 200
            time.sleep(self.scroll_pause_seconds)

            # Scroll n times to load more posts
            for _ in range(2):
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
                return []

            all_tweets = []
            for status in status_elements:
                try:
                    # Extract the aria-label attribute (contains all post info)
                    tweet_elem = status.find_element(By.XPATH, "./div[@aria-label]")
                    tweet_text = tweet_elem.get_attribute("aria-label").strip()
                    # tweet_text = "BUY BITCOIN NOW"
                    content_hash = hashlib.md5(f"{tweet_text}".encode()).hexdigest()
                    post_id = f"{content_hash}"

                    # Enrich timestamp information for json parsing
                    if tweet_text:
                        all_tweets.append(
                            {
                                "id": post_id,
                                "username": username,
                                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                                "content": tweet_text,
                            }
                        )
                except (
                    AttributeError,
                    NoSuchElementException,
                    StaleElementReferenceException,
                ) as e:
                    print("Error extracting post data: ", e)
                    continue

            return all_tweets if all_tweets else []

        except (TimeoutException, WebDriverException, NoSuchElementException) as e:
            print("Error trying to scrape the site: ", e)
            return []
        finally:
            try:
                driver.quit()
            except:
                pass
