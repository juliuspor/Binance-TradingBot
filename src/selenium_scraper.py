import time

from bs4 import BeautifulSoup
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
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.status__wrapper"))
        )

        SCROLL_PAUSE_SEC = 1
        last_height = driver.execute_script("return document.body.scrollHeight")
        for _ in range(5):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_SEC)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        all_posts = soup.select("div.status__wrapper")
        if not all_posts:
            print("No posts found. CSS might have changed.")
            return None, driver

        all_tweets = []
        for post_div in all_posts:
            content_div = post_div.select_one("div.status__content-wrapper")
            if content_div:
                post_text = content_div.get_text(separator="\n", strip=True)
                all_tweets.append(post_text)

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
