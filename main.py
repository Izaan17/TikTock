from cli import create_parser
from display import DisplayManager
from download_manager import DownloadManager
from extractors import URLExtractor
from tiktok_downloader import TikTokDownloader


def main() -> None:
    """
    The entry point of the program.
    """
    parser = create_parser()
    args = parser.parse_args()

    display = DisplayManager()
    tiktok_downloader = TikTokDownloader()
    download_manager = DownloadManager(display_manager=display, tiktok_downloader=tiktok_downloader)

    all_urls = []

    # Collect URLs from command line
    if args.urls:
        all_urls.extend(args.urls)

    # Collect URLs from a file if --recursive is used
    if args.recursive:
        try:
            extracted_urls = URLExtractor.extract_urls_from_file(parser, args.recursive, args)
            all_urls.extend(extracted_urls)
        except ValueError as e:
            parser.error(f"Error extracting URLs: {e}")
        except Exception as e:
            parser.error(f"Oops an unknown error occurred: {e}")

    if not all_urls:
        parser.error("No URLs provided to download.")

    # Validate URLs
    valid_urls = []
    for url in all_urls:
        if not tiktok_downloader.valid_url(url):
            print(f"\t{url} is not a valid TikTok URL!")
        else:
            valid_urls.append(url)

    if not valid_urls:
        parser.error("No valid TikTok URLs to download.")

    # Display summary
    print(f"\n> TikTok Video Downloader \n")
    print(f"[+] Author     : Izaan Noman")
    print(f"[+] URLs       : {len(all_urls)}")
    print(f"[+] Valid URLs : {len(valid_urls)}\n")

    # Download all valid URLs
    download_manager.download(
        valid_urls,
        args.output,
        args.delay,
        args.chunk_size,
        log_handler=args.log,
        filename_from_index=args.use_index
    )


if __name__ == "__main__":
    main()
