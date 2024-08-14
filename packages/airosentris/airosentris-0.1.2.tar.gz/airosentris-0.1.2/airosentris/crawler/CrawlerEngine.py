import os
from dotenv import load_dotenv
from airosentris.crawler.apify.ApifyCrawler import ApifyCrawler

load_dotenv()


class CrawlerEngine:

    def __init__(self, method: str = 'apify'):
        self.method = method

        if method == 'apify':
            apify_token = os.getenv('APIFY_TOKEN')
            if not apify_token:
                raise ValueError("APIFY_TOKEN environment variable is not set.")
            self.crawler = ApifyCrawler(apify_token)
        elif method == 'graphapi':
            raise NotImplementedError("GraphAPI method is not implemented yet.")
        elif method == 'instaloader':
            raise NotImplementedError("Instaloader method is not implemented yet.")
        elif method == 'selenium':
            raise NotImplementedError("Selenium method is not implemented yet.")
        else:
            raise ValueError(f"Unsupported crawling method: {method}")

    def get_instagram_post(self, username: str, date: str, limit: int):
        """
        Retrieves Instagram posts for a given username.

        Parameters:
        username (str): The Instagram username to fetch posts for.
        date (str): The date to filter posts.
        limit (int): The maximum number of posts to retrieve.

        Returns:
        list: A list of Instagram posts.
        """
        return self.crawler.get_instagram_post(username, date, limit)

    def get_instagram_comment(self, post_short_code: str, include_reply: bool):
        """
        Retrieves comments for a given Instagram post.

        Parameters:
        post_short_code (str): The short code of the Instagram post.
        include_reply (bool): Whether to include replies to comments.

        Returns:
        list: A list of Instagram comments.
        """
        return self.crawler.get_instagram_comment(post_short_code, include_reply)