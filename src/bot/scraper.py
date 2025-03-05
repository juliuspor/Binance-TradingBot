from dotenv import load_dotenv
import os
import subprocess

load_dotenv()

username = os.getenv("TRUTHSOCIAL_USERNAME")
password = os.getenv("TRUTHSOCIAL_PASSWORD")

def fetch_trump_tweets(username):
    print("fetching Trump Truth Social Posts")

    try:
        result = subprocess.run(
        ["truthbrush", "statuses", username], 
            capture_output=True, 
            text=True
        )
    except Exception as e: 
        print("Error fetching Trump tweets: ", e)
        return None
    
trump_username = "realDonaldTrump"  # Change if different
posts = fetch_trump_tweets(trump_username)
print(posts)    