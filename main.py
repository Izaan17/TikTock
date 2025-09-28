from rich.panel import Panel
from rich.table import Table

from cli import create_parser
from display import DisplayManager
from download_manager import DownloadManager
from extractors import URLExtractor
from tiktok_downloader import TikTokDownloader
from tiktok_helpers import is_valid_url


def main() -> None:
    """
    The entry point of the program.
    """
    parser = create_parser()
    args = parser.parse_args()

    display = DisplayManager()
    tiktok_downloader = TikTokDownloader()
    download_manager = DownloadManager(display_manager=display, tiktok_downloader=tiktok_downloader)

    urls = []

    # Collect URLs from command line
    if args.urls:
        urls.extend(args.urls)

    # Collect URLs from a file if --recursive is used
    if args.recursive:
        try:
            extracted_urls = URLExtractor.extract_urls_from_file(parser, args.recursive, args)
            urls.extend(extracted_urls)
        except ValueError as e:
            parser.error(f"Error extracting URLs: {e}")
        except Exception as e:
            parser.error(f"Oops an unknown error occurred: {e}")

    if not urls:
        parser.error("No URLs provided to download.")

    # Validate URLs
    valid_urls = []
    for url in urls:
        if not is_valid_url(url):
            print(f"\t{url} is not a valid TikTok URL!")
        else:
            valid_urls.append(url)

    if not valid_urls:
        parser.error("No valid TikTok URLs to download.")

    # Display summary
    summary_table = Table.grid(padding=(0, 2))
    summary_table.add_column(no_wrap=True)
    summary_table.add_column()

    summary_table.add_row("Valid URLs", str(len(valid_urls)))
    summary_table.add_row("Invalid URLs", str(len(urls) - len(valid_urls)))
    summary_table.add_row("Total URLs", str(len(urls)))
    summary_table.add_row("Author", "Izaan Noman")

    display.console.print(Panel(summary_table, title="TikTok Video Downloader", expand=True))
    display.console.print()

    # Download all valid URLs
    download_manager.download(
        valid_urls,
        args.output,
        args.delay,
        args.chunk_size,
        log_handler=args.log,
        filename_template=args.name_template
    )


if __name__ == "__main__":
    main()
