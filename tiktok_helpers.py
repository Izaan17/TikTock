import re


def get_video_author(url: str) -> str:
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
