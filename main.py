import argparse
import json
import os.path

from arg_types import dir_type
from downloader import TikTokDownloader
from extractors import TikTokActivityType, JSONExtractor, TextExtractor
from utils import select_from_choices


def create_parser() -> argparse.ArgumentParser:
    """
    Creates the parser with arguments.
    :return: The configured parser
    """
    parser = argparse.ArgumentParser(description="TikTok Video Downloader")

    # Positional arguments for URLs
    parser.add_argument("urls", nargs="*", metavar="TIKTOK_URLS", help="List of TikTok video URLs")

    # Optional argument for output folder (with default current datetime as file name)
    parser.add_argument("-o", "--output", type=dir_type, metavar="FOLDER_OUTPUT", default=f".",
                        help="Directory to save the downloaded videos")

    # Optional argument for a recursive file (e.g., a file with a list of URLs)
    parser.add_argument("-r", "--recursive", type=argparse.FileType('r'),  # Open the file in read mode
                        metavar="RECURSIVE", help="File containing a list of TikTok URLs to download recursively")

    return parser


def download(args: argparse.Namespace, tiktok_downloader: TikTokDownloader, urls: list[str]) -> None:
    """
    Wrapper function for downloading TikTok videos.
    :param args: The argparse namespace
    :param tiktok_downloader: The TikTok downloader instance
    :param urls: The urls to download
    :return: None
    """
    failed = []
    completed = []

    def on_progress(downloaded, total):
        progress = (downloaded / total) * 100
        status = '~' if downloaded != total else '✓'
        print(f"{status} {progress:.2f}%", end="\r")

        if downloaded == total:
            print()

    try:
        for i, url in enumerate(urls, start=1):
            print(f"==> Downloading [{i}/{len(urls)}] {url}")
            tiktok_id = f"{url.split('/')[-2]}"
            response = tiktok_downloader.download(url, output_path=os.path.join(args.output, f"{tiktok_id}.mp4"),
                                                  on_progress=on_progress)

            # Print status, error (if any), path, and size after download
            success = 'Success' if response.get('success', None) else 'Failed'
            error = f"Error: {response.get('error', '')} | " if response.get('error') else ''
            path = response.get('path', 'No path given')
            size = response.get('size')

            print(f"Status: {success} | {error}Output: {path} | Size: {size} |")
            print()

            if error != "":
                failed.append(tiktok_id)
            else:
                completed.append(tiktok_id)
    except KeyboardInterrupt:
        print("Exiting...")

    if failed:
        print(f"{len(failed)} videos failed to download.")

    if completed:
        print(f"{len(completed)} videos have downloaded successfully.")


def extract_urls_from_file(parser, file_handler) -> list[str]:
    """
    Wrapper class for extracting urls to each specified format
    :param parser: The current argument parser
    :param file_handler: The file handler
    :return: A list of a valid TikTok URLs based on the file handlers file extension
    """
    file_ext = os.path.splitext(file_handler.name)[1].lower()

    if file_ext == '.json':
        return handle_json_file(parser, file_handler)
    elif file_ext == '.txt':
        return handle_txt_file(file_handler)
    else:
        raise ValueError(f"Unsupported file type '{file_ext}'")


def handle_json_file(parser, file_handler) -> list[str]:
    """
    The wrapper class for extracting TikTok video URLs from a json file
    :param parser: The current argument parser
    :param file_handler: The file handler
    :return: A list of valid TikTok URLs
    """
    json_extractor = JSONExtractor()
    json_data = json.load(file_handler)

    if json_extractor.is_tiktok_format(json_data):
        selected_activities = select_from_choices("Select TikTok activities:", TikTokActivityType.get_all_types(),
                                                  allow_multiple=True)
        selected_activities = [TikTokActivityType.from_string(activity) for activity in selected_activities]
        if not selected_activities:
            parser.error("User did not specify any TikTok activity")

        # Flattening using list comprehension
        return [item for activity in selected_activities for item in
                json_extractor.extract_from_tiktok_format(json_data, activity)]

    return json_extractor.extract_from_custom_json_format(json_data)


def handle_txt_file(file_handler) -> list[str]:
    """
    The wrapper class for extracting TikTok video URLs from a text file
    :param file_handler: The file handler
    :return: A list of valid TikTok URLs
    """
    extractor = TextExtractor()
    return extractor.extract(file_handler)


def main() -> None:
    """
    The entry point of the program.
    :return: None
    """
    parser = create_parser()
    args = parser.parse_args()
    tiktok_downloader = TikTokDownloader()

    if args.urls:
        print(f"> TikTok Video Downloader ")
        print(f"> URLS ({len(args.urls)})")

        # Create a new list for valid URLs
        valid_urls = []

        for i, url in enumerate(args.urls):
            if not tiktok_downloader.valid_url(url):
                print(f"\t{url} is not a valid TikTok URL!")
            else:
                valid_urls.append(url)

        # Update args.urls with the valid URLs only
        args.urls = valid_urls
        print(f"> Valid URLS ({len(args.urls)})")

        download(args, tiktok_downloader, valid_urls)

    if args.recursive:
        try:
            urls = extract_urls_from_file(parser, args.recursive)
        except ValueError as e:
            parser.error(f"Error extracting URLs: {e}")

        if not urls:
            parser.error(f"No valid URLs found in '{args.recursive.name}'")

        download(args, tiktok_downloader, urls)


if __name__ == '__main__':
    main()
