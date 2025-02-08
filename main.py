from cli import create_parser
from display import DisplayManager
from download_manager import DownloadManager
from extractors import URLExtractor
from tiktok_downloader import TikTokDownloader


def main() -> None:
    """
    The entry point of the program.
    :return: None
    """
    parser = create_parser()
    args = parser.parse_args()

    display = DisplayManager()
    tiktok_downloader = TikTokDownloader()
    download_manager = DownloadManager(display, tiktok_downloader)

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

        download_manager.download(valid_urls, args.output, args.delay, args.chunk_size)

    if args.recursive:
        try:
            urls = URLExtractor.extract_urls_from_file(parser, args.recursive, args)
        except ValueError as e:
            parser.error(f"Error extracting URLs: {e}")

        if not urls:
            parser.error(f"No valid URLs found in '{args.recursive.name}'")

        download_manager.download(urls, args.output, args.delay, args.chunk_size, args.log)


if __name__ == '__main__':
    main()
