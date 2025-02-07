from enum import Enum
from typing import TextIO

from downloader import TikTokDownloader


class TikTokActivityType(Enum):
    """Types of TikTok activities that can be extracted."""
    FAVORITES = "Favorite Videos"
    LIKES = "Liked List"

    @classmethod
    def get_all_types(cls) -> list[str]:
        return [activity_type.value for activity_type in cls]

    @classmethod
    def from_string(cls, value: str) -> 'TikTokActivityType':
        for member in cls:
            if member.value == value:
                return member
        raise ValueError(f"Invalid activity type: {value}")


class JSONExtractor:
    """Extracts video URLs from JSON files."""

    @staticmethod
    def is_tiktok_format(data: dict) -> bool:
        """
        Check if the JSON parsed data is in the TikTok JSON format
        :param data: The JSON data to check
        :return: True if the data has the keys that constitute the TikTok JSON format, False otherwise
        """
        return 'Activity' in data

    @staticmethod
    def extract_from_custom_json_format(data: dict) -> list[str]:
        """
        Extracts TikTok video URLs from the custom json format of {'urls': ['https://tiktok.com/url1',]}
        :param data: The parsed JSON data
        :return: The valid TikTok URLs in the data
        """
        return [url for url in data.get('urls', []) if TikTokDownloader.valid_url(url)]

    def extract_from_tiktok_format(self, data: dict, activity_type: TikTokActivityType) -> list[str]:
        """
        Extracts TikTok video URLs from the TikTok download data format
        :param data: The parsed JSON data
        :param activity_type: The activities type (Favorites, Liked Videos)
        :return: The valid TikTok URLs corresponding to the activity type
        """
        activity = data.get('Activity', {})
        if activity_type == TikTokActivityType.FAVORITES:
            return self._extract_videos(activity.get('Favorite Videos', {}), 'FavoriteVideoList')

        return self._extract_videos(activity.get('Liked List', {}), 'ItemFavoriteList')

    @staticmethod
    def _extract_videos(activity_section: dict, key: str) -> list[str]:
        """
        Extracts TikTok video URLs from the nested JSON data
        :param activity_section: Which section to get the data from
        :param key: The key in which to get the video URLs
        :return: The valid TikTok URLs corresponding to the activity section
        """
        return [video.get('Link') for video in activity_section.get(key, []) if
                TikTokDownloader.valid_url(video.get('Link'))]


class TextExtractor:
    """Extracts video URLs from text files."""

    @staticmethod
    def extract(file_handler: TextIO) -> list[str]:
        """
        Extracts valid TikTok urls from a text file
        :param file_handler: The file handler
        :return: The valid TikTok URLs in the text file
        """
        return [url.strip() for url in file_handler.readlines() if TikTokDownloader.valid_url(url.strip())]
