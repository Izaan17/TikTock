import argparse

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
                        help="Directory to save the downloaded videos")

    parser.add_argument("-r", "--recursive", type=argparse.FileType('r'), metavar="RECURSIVE",
                        help="File containing a list of TikTok URLs to download recursively")

    parser.add_argument("-d", "--delay", type=int, metavar="DELAY", help="The delay before each download", default=1)

    parser.add_argument("-c", "--chunk-size", type=int, metavar="CHUNK_SIZE", help="The write speed of each download",
                        default=1024)

    parser.add_argument("--activity", nargs="+", choices=TikTokActivityType.get_all_types(), metavar="TIKTOK_ACTIVITY",
                        help="Pre select an activity", default=[])

    parser.add_argument("--log", type=argparse.FileType('w'), metavar="FILE_NAME",
                        help="Save a JSON log of the completed and failed URLs", const="tiktock_log.json", nargs="?")

    return parser
