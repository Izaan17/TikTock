import re
import requests
from urllib.parse import urlparse


def unshorten_url(url: str) -> str:
    """
    Unshortens a TikTok URL (e.g., tiktok.com/t/...) to get the full URL with author info.
    :param url: The URL to unshorten
    :return: The full unshortened URL, or the original URL if unshortening fails or is not needed
    """
    # Check if this is a shortened URL pattern (tiktok.com/t/...)
    if re.search(r'tiktok\.com/t/', url):
        try:
            # Use HEAD request to follow redirects without downloading content
            response = requests.head(url, allow_redirects=True, timeout=10)
            return response.url
        except requests.RequestException:
            # If unshortening fails, return the original URL
            return url

    # Not a shortened URL, return as is
    return url


def extract_video_id(url: str) -> str:
    """
    Extracts the video ID from a TikTok URL.
    :param url: The URL to extract the ID from
    :return: The video ID
    """
    parsed_url = urlparse(url)
    path = parsed_url.path.rstrip('/')  # remove trailing slash if any
    return path.split('/')[-1]


def extract_video_author(url: str) -> str:
    """
    Extracts the video author from a TikTok URL.
    :param url: The URL to get the author from
    :return: Video author's name
    """
    # Unshorten the URL first if it's a shortened link
    full_url = unshorten_url(url)

    # Use regex to capture the username in the URL
    match = re.search(r"@([a-zA-Z0-9_]+)", full_url)
    if match:
        return match.group(1)

    return "Unknown"


def is_valid_url(url: str) -> bool:
    """
    Validate the given URL if it is a TikTok URL.
    :param url: URL to validate
    :return: True if a TikTok URL, False otherwise
    """
    tiktok_pattern = r'https?://((?:vm|vt|www|v)\.)?tiktok(?:v)?\.com/.*'
    return bool(re.match(tiktok_pattern, url))
