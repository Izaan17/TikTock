import json
import os.path
from typing import TextIO

from display import DisplayManager
from tiktok_downloader import TikTokDownloader


class DownloadManager:
    """Class for connecting all components such as displaying, and downloading TikTok videos"""

    def __init__(self, display_manager: DisplayManager, tiktok_downloader: TikTokDownloader):
        self.display_manager = display_manager
        self.tiktok_downloader = tiktok_downloader

    def download(self, urls: list[str], output_path: str, delay: int, chunk_size: int,
                 log_handler: TextIO | None = None):
        data = {"completed": [], "failed": []}
        completed = data["completed"]
        failed = data["failed"]
        try:
            for i, url in enumerate(urls, start=1):
                response = self._download_video(url, output_path, delay, chunk_size, i, len(urls))
                self.display_manager.show_response_table(response)
                if response['success']:
                    completed.append(url)
                else:
                    failed.append((url, response.get('error', 'Unknown error')))
        except KeyboardInterrupt:
            self.display_manager.console.print("\n[bold yellow]Download interrupted[/]")

        self.display_manager.show_summary(completed, failed)

        if log_handler:
            json.dump(data, log_handler)

    def _download_video(self, url: str, output_path: str, delay: int, chunk_size: int, index: int, total: int):
        video_id = url.split('/')[-2]
        output_file = os.path.join(output_path, f"{video_id}.mp4")

        with self.display_manager.show_progress() as progress:
            task = progress.add_task("download", filename=f"{index} of {total}")

            def update_progress(downloaded: int, total_bytes: int):
                progress.update(task, completed=(downloaded / total_bytes) * 100)

            response = self.tiktok_downloader.download(url, output_file, on_progress=update_progress, delay=delay,
                                                       chunk_size=chunk_size)
            return response
