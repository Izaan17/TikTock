import argparse
from datetime import datetime

from arg_types import dir_type
from models import TikTokActivityType


def create_parser() -> argparse.ArgumentParser:
    """
    Creates the parser with arguments.
    :return: The configured parser
    """
    parser = argparse.ArgumentParser(description="TikTok Video Downloader")
    # Positional arguments
    parser.add_argument("urls", nargs="*", metavar="TIKTOK_URLS", help="List of TikTok video URLs")

    # Optional arguments
    parser.add_argument("-o", "--output", type=dir_type, metavar="FOLDER_OUTPUT", default=f".",
                        help="Directory to save the downloaded videos to")

    parser.add_argument("-r", "--recursive", type=argparse.FileType('r'), metavar="FILE_NAME",
                        help="A JSON or text file name which contains a list of TikTok URLs to download")

    parser.add_argument("-d", "--delay", type=int, metavar="DELAY", help="The delay before each download", default=0)

    parser.add_argument("-c", "--chunk-size", type=int, metavar="CHUNK_SIZE", help="The write speed of each download",
                        default=1024)

    parser.add_argument("--activity", nargs="+", choices=TikTokActivityType.get_all_types(), metavar="TIKTOK_ACTIVITY",
                        help="Pre select an activity", default=[])

    parser.add_argument("--log", type=argparse.FileType('w'), metavar="FILE_NAME",
                        help="Save a JSON log of the completed and failed URLs",
                        const=f"{datetime.now().strftime("[tiktock] %Y-%m-%d_%H-%M_log.json")}", nargs="?")

    parser.add_argument(
        "--use-index",
        action="store_true",
        help="Use the download index as the filename instead of the TikTok video ID"
    )

    return parser
