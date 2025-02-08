import argparse
import json
import os
import os.path

from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn
from rich.table import Table

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

    return parser


def get_tiktok_id(url: str) -> str:
    """Extracts TikTok ID from URL."""
    return url.split("/")[-2]


def generate_response_table(response: dict) -> Table:
    """Generates a table displaying the download results for a single video."""
    success = '✓' if response.get('success') else '𐄂'
    status_color = "green" if success == '✓' else "red"
    error = response.get('error', '')
    path = response.get('path', 'None')
    size = str(response.get('size', 'None'))
    url = response.get('url', 'None')

    table = Table(show_header=False, box=None)
    table.add_column(style="bold")

    table.add_row("Status:", f"[bold {status_color}]{success}[/]")
    table.add_row("URL:", url)
    table.add_row("Output:", path)
    table.add_row("Size:", size)
    if error:
        table.add_row("[red]Error[/]:", error)

    return table


def generate_summary_table(completed: list[str], failed: list[tuple[str, str]]) -> Table:
    """Generates the final summary table showing overall download results."""
    table = Table(title="Download Summary", show_header=True, header_style="bold")
    table.add_column("Total URLs Attempted", justify="right")
    table.add_column("Successfully Downloaded", justify="right")
    table.add_column("Failed Downloads", justify="right")
    table.add_row(f"{len(completed) + len(failed)}", f"[green]{len(completed)}", f"[red]{len(failed)}", )
    return table


def generate_failed_table(failed: list[tuple[str, str]]) -> Table:
    """Generates a table showing details of failed downloads."""
    failed_table = Table(show_header=True, header_style="bold")
    failed_table.add_column("No.", style="bold cyan", justify="right")
    failed_table.add_column("URL", style="bold")
    failed_table.add_column("Error", style="bold red")

    for i, (url, error) in enumerate(failed, start=1):
        failed_table.add_row(str(i), f"[bold]{url}[/]", f"[red]{error}[/]")

    return failed_table


def download_single_video(url: str, output_file: str, downloader: TikTokDownloader, delay: int, chunk_size: int,
                          index: int, total: int, console: Console) -> dict:
    """Handles the download of a single video with progress tracking."""
    with Progress(TextColumn("[bold]Downloading {task.fields[filename]}", justify="right"), BarColumn(bar_width=None),
                  "[white]{task.percentage:>3.1f}%", TimeRemainingColumn(), console=console) as progress:
        task = progress.add_task("download", filename=f"{index} of {total}")

        def on_progress(downloaded: int, total_bytes: int):
            progress.update(task, completed=(downloaded / total_bytes) * 100)

        return downloader.download(url, output_path=output_file, on_progress=on_progress, delay=delay,
                                   chunk_size=chunk_size)


def download(args: argparse.Namespace, tiktok_downloader: TikTokDownloader, urls: list[str]) -> None:
    """Main download handler coordinating the download process and reporting."""
    console = Console()
    failed = []
    completed = []

    try:
        for i, url in enumerate(urls, start=1):
            tiktok_id = get_tiktok_id(url)
            output_file = os.path.join(args.output, f"{tiktok_id}.mp4")

            response = download_single_video(url=url, output_file=output_file, downloader=tiktok_downloader,
                                             delay=args.delay, chunk_size=args.chunk_size, index=i, total=len(urls),
                                             console=console)

            console.print(generate_response_table(response))

            if response.get('error'):
                failed.append((url, response['error']))
            else:
                completed.append(tiktok_id)

    except KeyboardInterrupt:
        console.print("\n[bold yellow]Download interrupted by user.[/]")

    # Show summary of results
    console.print(generate_summary_table(completed, failed))

    # Show failed downloads details if any
    if failed:
        console.print("\n[bold]Details of Failed Downloads:[/]")
        console.print(generate_failed_table(failed))
        console.print(f"[bold]Total[/]: {len(failed)} videos failed to download.\n")


def extract_urls_from_file(parser, file_handler, args) -> list[str]:
    """
    Wrapper class for extracting urls to each specified format
    :param parser: The current argument parser
    :param file_handler: The file handler
    :param args: Parser arguments
    :return: A list of a valid TikTok URLs based on the file handlers file extension
    """
    file_ext = os.path.splitext(file_handler.name)[1].lower()

    if file_ext == '.json':
        return handle_json_file(parser, file_handler, args)
    elif file_ext == '.txt':
        return handle_txt_file(file_handler)
    else:
        raise ValueError(f"Unsupported file type '{file_ext}'")


def handle_json_file(parser, file_handler, args) -> list[str]:
    """
    Extracts TikTok video URLs from a JSON file.

    :param parser: Argument parser instance
    :param file_handler: File handler object
    :param args: Parser arguments
    :return: A list of valid TikTok URLs
    """
    json_extractor = JSONExtractor()
    json_data = json.load(file_handler)

    if not json_extractor.is_tiktok_format(json_data):
        return json_extractor.extract_from_custom_json_format(json_data)

    selected_activities = args.activity or prompt_for_activities()

    if not selected_activities:
        parser.error("User did not specify any TikTok activity")

    # Flatten the list to convert them into TikTok Activity Types
    selected_activities = [TikTokActivityType.from_string(activity) for activity in selected_activities]

    return [item for activity in selected_activities for item in
            json_extractor.extract_from_tiktok_format(json_data, activity)]


def prompt_for_activities() -> list[str]:
    """
    Prompts the user to select TikTok activities.
    :return: List of activities
    """
    print("TikTok User Download Data Detected")
    print("Please select the following activities to download videos from")
    return select_from_choices("Select TikTok activities", TikTokActivityType.get_all_types(), allow_multiple=True)


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
            urls = extract_urls_from_file(parser, args.recursive, args)
        except ValueError as e:
            parser.error(f"Error extracting URLs: {e}")

        if not urls:
            parser.error(f"No valid URLs found in '{args.recursive.name}'")

        download(args, tiktok_downloader, urls)


if __name__ == '__main__':
    main()
