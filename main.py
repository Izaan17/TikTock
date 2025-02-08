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


def download(args: argparse.Namespace, tiktok_downloader: TikTokDownloader, urls: list[str]) -> None:
    """
    Wrapper function for downloading TikTok videos with enhanced output using rich.
    :param args: The argparse namespace
    :param tiktok_downloader: The TikTok downloader instance
    :param urls: The urls to download
    :return: None
    """
    failed = []
    completed = []
    console = Console()

    try:
        for i, url in enumerate(urls, start=1):
            tiktok_id = f"{url.split('/')[-2]}"
            output_file = os.path.join(args.output, f"{tiktok_id}.mp4")

            # Initialize the progress bar for this download
            with Progress(TextColumn("[bold]Downloading {task.fields[filename]}", justify="right"),
                          BarColumn(bar_width=None), "[white]{task.percentage:>3.1f}%", TimeRemainingColumn(),
                          console=console) as progress:
                task = progress.add_task("download", filename=f"{i} of {len(urls)}")

                def on_progress(downloaded, total):
                    # Update the progress bar based on the percentage completed
                    progress.update(task, completed=(downloaded / total) * 100)

                # Perform the download
                response = tiktok_downloader.download(url, output_path=output_file, on_progress=on_progress,
                                                      delay=args.delay, chunk_size=args.chunk_size)

            # Print status, error (if any), path, and size after the progress bar
            success = '✓' if response.get('success', None) else '𐄂'
            status_color = "green" if success == '✓' else "red"
            error = response.get('error', '')
            path = response.get('path', 'None')
            size = str(response.get('size', 'None'))

            response_table = Table(show_header=False, box=None)
            response_table.add_column(style="bold")

            response_table.add_row("Status:", f"[bold {status_color}]{success}[/]")
            response_table.add_row("URL:", url)
            response_table.add_row("Output:", path)
            response_table.add_row("Size:", size)
            if error != '':
                response_table.add_row("[red]Error[/]:", error)

            console.print(response_table)

            if error != "":
                failed.append((url, response.get('error', '')))
            else:
                completed.append(tiktok_id)

    except KeyboardInterrupt:
        console.print("\n[bold yellow]Download interrupted by user.[/]")

    # Summary table
    table = Table(title="Download Summary", show_header=True, header_style="bold")
    table.add_column("Total URLs Attempted", justify="right")
    table.add_column("Successfully Downloaded", justify="right")
    table.add_column("Failed Downloads", justify="right")
    table.add_row(f"{len(completed) + len(failed)}", f"[green]{len(completed)}", f"[red]{len(failed)}")

    console.print(table)

    if failed:
        console.print("\n[bold]Details of Failed Downloads:[/]")

        # Create a table to display failed downloads
        failed_table = Table(show_header=True, header_style="bold")
        failed_table.add_column("No.", style="bold cyan", justify="right")
        failed_table.add_column("URL", style="bold")  # Adjust width as needed
        failed_table.add_column("Error", style="bold red")

        # Add rows for each failed video
        for i, video_tuple in enumerate(failed, start=1):
            url, error = video_tuple
            failed_table.add_row(str(i), f"[bold]{url}[/]", f"[red]{error}[/]")

        # Print the table with all failed download details
        console.print(failed_table)

        # Print total number of failed downloads
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
