import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


def fetch_all_tweets(username="realDonaldTrump"):
    url = f"https://truthsocial.com/@{username}"
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.6998.45 Safari/537.36"
    )
    # chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=chrome_options
    )

    try:
        driver.get(url)
        # Wait for at least one tweet container to be present
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div[data-testid='status']")
            )
        )

        SCROLL_PAUSE_SEC = 4
        last_height = driver.execute_script("return document.body.scrollHeight")
        scroll_amount = 600
        time.sleep(SCROLL_PAUSE_SEC)

        # Scroll a few times to load more tweets
        for i in range(3):
            driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
            time.sleep(SCROLL_PAUSE_SEC)

            # Save a snapshot of the page if needed
            with open(f"page_snapshot_{i}.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)

            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                # Try one more scroll if the page did not grow
                driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
            time.sleep(SCROLL_PAUSE_SEC)
            last_height = driver.execute_script("return document.body.scrollHeight")

        # Iterate through each tweet container and get the immediate child with aria-label
        status_elements = driver.find_elements(
            By.CSS_SELECTOR, "div[data-testid='status']"
        )
        if not status_elements:
            print("No tweets found. The CSS selectors might have changed.")
            return None, driver

        all_tweets = []
        for status in status_elements:
            try:
                # Using XPath to get the direct child element that holds the tweet text
                tweet_elem = status.find_element(By.XPATH, "./div[@aria-label]")
                tweet_text = tweet_elem.get_attribute("aria-label").strip()
                if tweet_text:
                    all_tweets.append(tweet_text)
            except Exception as e:
                # If no direct child with aria-label is found, skip this container
                continue

        return (all_tweets if all_tweets else None), driver

    except Exception as e:
        print("Error:", e)
        return None, driver


if __name__ == "__main__":
    tweets, driver = fetch_all_tweets()
    if tweets:
        print("\nALL TWEETS:")
        for idx, tweet in enumerate(tweets, 1):
            print(f"\nPost {idx}:\n{tweet}")
    else:
        print("No tweets found.")
    input("Press Enter to close the browser.")
