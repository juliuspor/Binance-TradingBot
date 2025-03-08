import json
import re
import subprocess

from base_scraper import BaseScraper


class TruthBrushScraper(BaseScraper):
    """
    Fetches posts using the 'truthbrush' CLI tool.
    """

    def fetch_latest_posts(self, username):
        """
        Fetch the latest posts from Truth Social for a given username.

        Uses 'truthbrush' to retrieve posts and parses the JSON output.

        Args:
            username (str): Truth Social username

        Returns:
            list: Up to 4 most recent posts as dictionaries, or None if failed
        """
        print(f"TruthBrush scraper: fetching the latest {username} Posts")

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
                return tweets[:3]

        except (subprocess.SubprocessError, json.JSONDecodeError) as e:
            print("Error fetching Trumps latest post: ", e)
            return None
        return None
