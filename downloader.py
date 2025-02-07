import re
import time
from typing import Callable

import requests


class TikTokDownloader:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5', 'Connection': 'keep-alive'}
        self.session = requests.Session()

    def _get_download_url(self, url: str) -> str:
        """
        Retrieves the direct download URL of a video from the given web page URL.
        It makes an HTTP request, searches for video URLs in the page source, cleans up
        the URL, and returns the download link.

        :param url: The URL of the page containing the video.
        :return: A string with the video download URL.
        :raises Exception: If there is an error fetching or processing the URL.
        """
        try:
            # First get the HTML page
            response = self.session.get(url, headers=self.headers)
            response.raise_for_status()

            # Try multiple patterns to find video URLs
            url_patterns = [r'"playAddr":"([^"]+)"',  # Play URL this url has no watermark
                            r'"downloadAddr":"([^"]+)"',  # Download URL has a watermark
                            r'"video":{"downloadAddr":"([^"]+)"'  # Alternate pattern not sure yet
                            ]

            video_urls = []
            for pattern in url_patterns:
                video_urls = re.findall(pattern, response.text)
                if video_urls:
                    break

            if not video_urls:
                raise Exception("Could not find video URL in page source")

            # Clean up the URL (remove backslashes)
            video_url = video_urls[0].encode().decode('unicode-escape')

            return video_url

        except Exception as e:
            raise Exception(f"Failed to get download URL: {str(e)}")

    @staticmethod
    def valid_url(url: str) -> bool:
        """
        Validate the given URL if it is a TikTok URL.
        :param url: URL to validate
        :return: True if a TikTok URL, False otherwise
        """
        tiktok_pattern = r'https?://((?:vm|vt|www|v)\.)?tiktok(?:v)?\.com/.*'
        return bool(re.match(tiktok_pattern, url))

    def download(self, url: str, output_path: str, on_progress: Callable[[int, int], None] = None,
                 block_size: int = 1024, delay: int = 1) -> dict[str, any]:
        """
        Downloads the video from the given TikTok URL and saves it to the specified output path.
        The function optionally reports download progress through the `on_progress` callback and allows configuring
        the block size for downloading the file in chunks. Additionally, a delay can be set between each request to reduce server load.

        :param url: The URL of the video to download.
        :param output_path: The file path where the downloaded content will be saved.
        :param on_progress: (Optional) A callback function that will be called with the number of bytes downloaded
                             and the total size of the file. The callback signature should be `on_progress(bytes_downloaded, total_size)`.
                             This parameter can be used to display or track download progress.
        :param block_size: (Optional) The size of each chunk of data to download in bytes. Default is 1024 bytes (1 KB).
                            A larger block size may increase download speed but use more memory.
        :param delay: (Optional) The delay in seconds between the request. Default is 1 second.
                      This can be used to reduce server load.

        :return: A dictionary with keys related to the download status. The dictionary can contain:
                 - 'success': A boolean indicating the result of the download process.
                 - 'path': The file path where the downloaded content is saved.
                 - 'url': The downloaded videos url.
                 - 'size': (Optional) The total size of the file downloaded if the download succeeds.
                 - 'error': (Optional) An error message if the download fails.
        """
        try:
            # Get video download URL
            video_url = self._get_download_url(url)

            # Add delay to avoid rate limiting
            time.sleep(delay)

            # Download video with proper headers
            response = self.session.get(video_url, headers=self.headers, stream=True)
            response.raise_for_status()

            # Save video
            total_size = int(response.headers.get('content-length', 0))
            bytes_downloaded = 0

            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=block_size):
                    if chunk:
                        f.write(chunk)
                        bytes_downloaded += len(chunk)

                        if on_progress and total_size:
                            on_progress(bytes_downloaded, total_size)

            return {'success': True, 'path': output_path, 'size': total_size, 'url': url}

        except Exception as e:
            return {'success': False, 'error': str(e), 'url': url}
