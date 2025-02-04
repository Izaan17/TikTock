# TikTock:
# An app that allows you to download all of your favorite videos before TikTok gets deleted.
import argparse
import os.path

from arg_types import dir_type
from downloader import TikTokDownloader
from extractor import VideoUrlExtractor


def create_parser() -> argparse.ArgumentParser:
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


def _download(args, tiktok_downloader: TikTokDownloader, urls):
    def on_progress(downloaded, total):
        progress = (downloaded / total) * 100
        status = '~' if downloaded != total else '✓'
        print(f"{status} {progress:.2f}%", end="\r")

        if downloaded == total:
            print()

    for i, url in enumerate(urls, start=1):
        # Print initial download information before attempting download
        print(f"==> Downloading [{i}/{len(urls)}] {url}")

        response = tiktok_downloader.download(url, output_path=os.path.join(args.output, f"{url.split('/')[-2]}.mp4"),
                                              on_progress=on_progress)

        # Print status, error (if any), path, and size after download
        success = 'Success' if response.get('success', None) else 'Failed'
        error = f"Error: {response.get('error', '')} |" if response.get('error') else ''
        path = response.get('path', 'No path given')
        size = response.get('size')

        print(f"Status: {success} | {error} Output: {path} | Size: {size} |")
        print()


def main():
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

        _download(args, tiktok_downloader, valid_urls)

    if args.recursive:
        file_handler = args.recursive
        urls = VideoUrlExtractor.extract_urls(args.recursive)
        if not urls:
            raise argparse.ArgumentError(None, f"No valid urls found in '{file_handler.name}'")

        _download(args, tiktok_downloader, urls)


if __name__ == '__main__':
    main()
