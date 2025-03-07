import json
import re
import subprocess


def fetch__n_latest_posts(username, number_of_tweets):
    """
    Fetch the latest posts from Truth Social for a given username.

    Uses 'truthbrush' to retrieve posts and parses the JSON output.

    Args:
        username (str): Truth Social username

    Returns:
        list: Up to 4 most recent posts as dictionaries, or None if failed
    """
    print("fetching the latest Trump Truth Social Post")

    try:
        result = subprocess.run(
            ["truthbrush", "statuses", username],
            capture_output=True,
            text=True,
            check=False,
        )
        output = result.stdout.strip()
        error_output = result.stderr.strip()

        print("error_output: ", error_output)
        if "cloudflare" in error_output.lower() or "cloudflare" in output.lower():
            print("Cloudflare protection detected. You may be blocked.")
        if re.search(r"\b(403|429|503|1020)\b", output) or re.search(
            r"\b(403|429|503|1020)\b", error_output
        ):
            print(
                "Possible Cloudflare restriction encountered. Response:",
                output or error_output,
            )

        if not output:
            print("No output received from truthbrush")
            return None

        tweets = []

        for line in output.split("\n"):
            try:
                tweet = json.loads(line)
                tweets.append(tweet)
            except json.JSONDecodeError as e:
                print("Error parsing tweet: ", e)
        if tweets:
            return tweets[:number_of_tweets]

    except (subprocess.SubprocessError, json.JSONDecodeError) as e:
        print("Error fetching Trumps latest post: ", e)
        return None
    return None
