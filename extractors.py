import json
import os
from typing import TextIO

from models import TikTokActivityType
from tiktok_downloader import TikTokDownloader
from utils import select_from_choices


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
        Extracts TikTok video URLs from the custom JSON format of {'urls': ['https://tiktok.com/url1']}
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


class URLExtractor:
    """Extracts URLS from various file types"""

    @staticmethod
    def handle_txt_file(file_handler) -> list[str]:
        """
        The wrapper class for extracting TikTok video URLs from a text file
        :param file_handler: The file handler
        :return: A list of valid TikTok URLs
        """
        extractor = TextExtractor()
        return extractor.extract(file_handler)

    @classmethod
    def extract_urls_from_file(cls, parser, file_handler, args) -> list[str]:
        """
        Wrapper class for extracting urls to each specified format
        :param parser: The current argument parser
        :param file_handler: The file handler
        :param args: Parser arguments
        :return: A list of a valid TikTok URLs based on the file handlers file extension
        """
        file_ext = os.path.splitext(file_handler.name)[1].lower()

        if file_ext == '.json':
            return cls.handle_json_file(parser, file_handler, args)
        elif file_ext == '.txt':
            return cls.handle_txt_file(file_handler)
        else:
            raise ValueError(f"Unsupported file type '{file_ext}'")

    @classmethod
    def handle_json_file(cls, parser, file_handler, args) -> list[str]:
        """
        Extracts TikTok video URLs from a JSON file.

        :param parser: Argument parser instance
        :param file_handler: File handler object
        :param args: Parser arguments
        :return: A list of valid TikTok URLs
        """
        json_extractor = JSONExtractor()
        json_data = json.load(file_handler)

        if not json_extractor.is_tiktok_format(json_data):
            return json_extractor.extract_from_custom_json_format(json_data)

        selected_activities = args.activity or cls.prompt_for_activities()

        if not selected_activities:
            parser.error("User did not specify any TikTok activity")

        # Flatten the list to convert them into TikTok Activity Types
        selected_activities = [TikTokActivityType.from_string(activity) for activity in selected_activities]

        return [item for activity in selected_activities for item in
                json_extractor.extract_from_tiktok_format(json_data, activity)]

    @staticmethod
    def prompt_for_activities() -> list[str]:
        """
        Prompts the user to select TikTok activities.
        :return: List of activities
        """
        print("TikTok User Download Data Detected")
        print("Please select the following activities to download videos from")
        return select_from_choices("Select TikTok activities", TikTokActivityType.get_all_types(), allow_multiple=True)
