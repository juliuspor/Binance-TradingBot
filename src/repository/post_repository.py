import json
import os
from datetime import datetime


class PostRepository:
    """
    Repository for storing and retrieving processed posts to prevent duplicate processing.
    """

    def __init__(self, storage_path="data/processed_posts.json"):
        """
        Initialize the repository with the path to the storage file.

        Args:
            storage_path (str): Path to the JSON file for storing processed posts
        """
        self.storage_path = storage_path
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)

        self.processed_posts = self._load_processed_posts()

    def _load_processed_posts(self):
        """Load processed posts from the storage file."""
        if not os.path.exists(self.storage_path):
            # Create empty file with an empty JSON object
            with open(self.storage_path, "w") as file:
                json.dump({}, file)
            return {}

        try:
            with open(self.storage_path, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            # If file exists but is corrupted, reset it
            with open(self.storage_path, "w") as file:
                json.dump({}, file)
            return {}

    def _save_processed_posts(self):
        """Save processed posts to the storage file."""
        with open(self.storage_path, "w") as file:
            json.dump(self.processed_posts, file, indent=4)

    def is_post_processed(self, post):
        """
        Check if a post has already been processed.

        Args:
            post (dict): Post dictionary containing content and other metadata

        Returns:
            bool: True if post has been processed before, False otherwise
        """
        # Using ID as the unique identifier
        post_id = post.get("id")

        return str(post_id) in self.processed_posts

    def mark_post_as_processed(self, post):
        """
        Mark a post as processed to avoid processing it again.

        Args:
            post (dict): Post dictionary containing content and other metadata
        """
        # Create a unique identifier for the post
        post_id = post.get("id")

        # Persist the post with processed timestamp
        self.processed_posts[str(post_id)] = {
            "id": post_id,
            "content": post["content"],
            "processed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "username": post.get("username"),
        }
        self._save_processed_posts()
