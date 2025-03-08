from abc import ABC, abstractmethod


class BaseScraper(ABC):
    """
    Abstract base class for Truth Social scrapers.
    """

    @abstractmethod
    def fetch_latest_posts(self, username):
        """
        Fetches the latest posts for a given username.
        Must be implemented by subclasses.
        """
        pass
