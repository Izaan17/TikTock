import json
import os.path

from display import DisplayManager
from tiktok_downloader import TikTokDownloader
from tiktok_helpers import extract_video_id
from utils import parse_filename_template


class DownloadManager:
    """Connects all components such as displaying, and downloading TikTok videos"""

    def __init__(self, display_manager: DisplayManager, tiktok_downloader: TikTokDownloader):
        self.display_manager = display_manager
        self.tiktok_downloader = tiktok_downloader

    def download(self, urls: list[str], output_path: str, delay: int, chunk_size: int,
                 log_handler: object | None = None, filename_template: str | None = None) -> None:
        """
        Downloads a list of videos with the progress bar with status information and a summary
        :param urls: The URLs to download
        :param output_path: The output folder
        :param delay: The delay between each download
        :param chunk_size: The chunk size write speed
        :param log_handler: If provided writes a log file of the completed and failed downloads
        :param filename_template: Template to design the file name
        :return: None
        """
        data = {"total": len(urls), "output": output_path, "delay": delay, "chunk_size": chunk_size,
                "filename_template": filename_template if filename_template else "None",
                "completed": [], "failed": []}
        completed = data["completed"]
        failed = data["failed"]
        try:
            for i, url in enumerate(urls, start=1):
                file_name = parse_filename_template(i, url, filename_template) if filename_template else None
                response = self._download_video(url, output_path, delay, chunk_size, i, len(urls),
                                                file_name=file_name)
                self.display_manager.show_response_table(response)
                if response['success']:
                    completed.append(url)
                else:
                    failed.append((url, response.get('error', 'Unknown error')))
        except KeyboardInterrupt:
            self.display_manager.console.print("\n[bold yellow]Download interrupted[/]")

        self.display_manager.show_summary(completed, failed)

        if log_handler:
            json.dump(data, log_handler, indent=4)

    def _download_video(self, url: str, output_path: str, delay: int, chunk_size: int, index: int, total: int,
                        file_name: str | None = None) -> dict:
        """
        Downloads a video with the display managers progress bar
        :param url: The url to download
        :param output_path: The folder in which the file will be stored
        :param delay: The delay before starting the download
        :param chunk_size: The writing speed of the transfer
        :param index: The current index of the download
        :param total: The total amount of downloads
        :return: Response dictionary
        """
        file_name = str(file_name) if file_name else extract_video_id(url)
        output_file = os.path.join(output_path, f"{file_name}.mp4")

        with self.display_manager.show_progress() as progress:
            task = progress.add_task("download", filename=f"{index} of {total}")

            def update_progress(downloaded: int, total_bytes: int):
                progress.update(task, completed=(downloaded / total_bytes) * 100)

            response = self.tiktok_downloader.download(url, output_file, on_progress=update_progress, delay=delay,
                                                       chunk_size=chunk_size)
            return response
