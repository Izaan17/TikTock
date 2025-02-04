import re
import time
from typing import Callable

import requests


class TikTokDownloader:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5', 'Connection': 'keep-alive', }
        self.session = requests.Session()

    def _get_download_url(self, url: str):
        """Get the actual watermark-free video download URL."""
        try:
            # First get the HTML page
            response = self.session.get(url, headers=self.headers)
            response.raise_for_status()

            # Try multiple patterns to find video URLs
            url_patterns = [r'"downloadAddr":"([^"]+)"',  # Download URL
                            r'"playAddr":"([^"]+)"',  # Play URL
                            r'"video":{"downloadAddr":"([^"]+)"'  # Alternate pattern
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

            # Replace watermarked URL with watermark-free version if possible
            video_url = video_url.replace('/watermark/', '/no-watermark/')

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

    def download(self, url, output_path, on_progress: Callable[[int, int], None] = None, block_size=1024, delay=1):
        """Download TikTok video to specified path without watermark."""
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


if __name__ == '__main__':
    # Create an instance
    downloader = TikTokDownloader()


    def on_progress(downloaded, total):
        print(f"Downloaded: {downloaded} / {total}")
        print(f"Progress: {(downloaded / total) * 100:.2f}%")


    # Download a video (replace with your desired TikTok video URL)
    r = downloader.download("https://www.tiktok.com/@username/video/xxxxxxxxxxxxxxxxx", "output_video.mp4", on_progress)
    print(r)
