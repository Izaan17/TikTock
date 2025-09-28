import re
from urllib.parse import urlparse


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
    # Use regex to capture the username in the URL
    match = re.search(r"@([a-zA-Z0-9_]+)", url)
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
