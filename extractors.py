from enum import Enum
from typing import TextIO

from downloader import TikTokDownloader


class TikTokActivityType(Enum):
    """Types of TikTok activities that can be extracted."""
    FAVORITES = "Favorite Videos"
    LIKES = "Like List"

    @classmethod
    def get_all_types(cls) -> list[str]:
        """Returns a list of all activity type values."""
        return [activity_type.value for activity_type in cls]

    @classmethod
    def from_string(cls, value: str) -> 'TikTokActivityType':
        """Converts a string to a TikTokActivityType enum."""
        try:
            return cls(value)
        except ValueError:
            raise ValueError(f"Invalid activity type: {value}")


class JSONExtractor:
    """Handles extraction of TikTok video URLs from JSON files."""

    @staticmethod
    def is_tiktok_format(data: dict) -> bool:
        """
        Checks if the provided data follows TikTok's JSON format.
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
        activity_section = self._get_activity_section(activity, activity_type)
        return self._extract_videos(activity_section, activity_type)

    @staticmethod
    def _get_activity_section(activity: dict, activity_type: TikTokActivityType) -> dict:
        """
        Fetches the relevant section of the activity based on the activity type.
        :param activity: The activity section
        :param activity_type: The type of activity
        :return:
        """
        if activity_type == TikTokActivityType.FAVORITES:
            return activity.get('Favorite Videos', {})
        return activity.get('Like List', {})

    @staticmethod
    def _extract_videos(activity_section: dict, activity_type: TikTokActivityType) -> list[str]:
        """
        Extracts TikTok video URLs from the nested JSON data
        :param activity_section: Which section to get the data from
        :param activity_type: The type of activity
        :return: The valid TikTok URLs corresponding to the activity section
        """
        key = 'FavoriteVideoList' if activity_type == TikTokActivityType.FAVORITES else 'ItemFavoriteList'
        video_url_key = 'Link' if activity_type == TikTokActivityType.FAVORITES else 'link'

        return [video.get(video_url_key) for video in activity_section.get(key, []) if
                TikTokDownloader.valid_url(video.get(video_url_key))]


class TextExtractor:
    """Extracts TikTok video URLs from text files."""

    @staticmethod
    def extract(file_handler: TextIO) -> list[str]:
        """
        Extracts valid TikTok urls from a text file
        :param file_handler: The file handler
        :return: The valid TikTok URLs in the text file
        """
        return [url.strip() for url in file_handler.readlines() if TikTokDownloader.valid_url(url.strip())]
