import json
import os
from typing import TextIO

from downloader import TikTokDownloader


class VideoUrlExtractor:
    """Handles extraction of video URLs from different file types."""

    @staticmethod
    def from_json(file_handler: TextIO) -> list[str]:
        """
        Extract video URLs from a JSON file.

        Supports two JSON formats:
        1. Custom JSON with an 'urls' key
        2. TikTok downloaded data format
        """
        try:
            data = json.load(file_handler)

            # Check for custom JSON format
            if custom_urls := data.get('urls'):
                return [url for url in custom_urls if TikTokDownloader.valid_url(url)]

            # Check for TikTok downloaded data format
            activity = data.get('Activity', {})
            favorite_videos = activity.get('Favorite Videos', {})
            video_list = favorite_videos.get('FavoriteVideoList', [])

            return [video_dict.get('Link') for video_dict in video_list if
                    TikTokDownloader.valid_url(video_dict.get('Link'))]

        except json.JSONDecodeError:
            return []

    @staticmethod
    def from_text(file_handler: TextIO) -> list[str]:
        """Extract video URLs from a text file."""
        return [url.strip() for url in file_handler.readlines() if TikTokDownloader.valid_url(url.strip())]

    @classmethod
    def extract_urls(cls, file_handler: TextIO) -> list[str]:
        """
        Determine the file type and extract URLs accordingly.

        Supports .json and .txt files.
        """
        file_ext = os.path.splitext(file_handler.name)[1].lower()

        url_extractors = {'.json': cls.from_json, '.txt': cls.from_text}

        extractor = url_extractors.get(file_ext)
        if not extractor:
            raise ValueError(f"Unsupported file type: {file_ext}")

        return extractor(file_handler)
