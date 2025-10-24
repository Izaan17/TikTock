import datetime
import string

from tiktok_helpers import extract_video_author, extract_video_id


def select_from_choices(prompt: str, choices: list, allow_multiple: bool = True) -> list:
    """
    Select from a list of options.
    :param prompt: The prompt to display to the user
    :param choices: The list of valid choices
    :param allow_multiple:  If True, allows the selection of multiple choices
    :return: The selected choice(s)
    """
    selected = []

    # Display choices
    def display_choices():
        for i, choice in enumerate(choices, start=1):
            print(f"({i}) {choice}")

    while True:
        if not allow_multiple and len(selected) >= 1:
            break  # Stop if only a single selection is allowed and already selected one item

        print(f"Selected items: {', '.join(selected)}" if selected else '', end='\n' if selected else '')
        display_choices()

        # Get valid user inputx
        try:
            user_choice = get_int(prompt=f"{prompt} (or press 0 to finish): ", min_bound=0, max_bound=len(choices))
            print()

            if user_choice == 0:
                if allow_multiple:  # If multiple selections allowed, break out only when a user opts to finish
                    break
                else:
                    return selected  # If not allowing multiple, finalize after 1 selection

            selected_choice_element = choices[user_choice - 1]

            if selected_choice_element in selected:
                selected.remove(selected_choice_element)  # Remove the item if already selected
            else:
                selected.append(selected_choice_element)  # Add the item if not selected

        except KeyboardInterrupt:
            break

    return selected


def get_int(prompt: str, min_bound: int, max_bound: int) -> int:
    """
    Prompt the user for an integer between the min and max bound set.
    :param prompt: The prompt to ask the user
    :param min_bound: The minimum allowed number (inclusive)
    :param max_bound: The maximum allowed number (inclusive)
    :return: A number between the min and max bound
    """
    while True:
        try:
            user_input = int(input(prompt))
            if min_bound <= user_input <= max_bound:
                return user_input
            else:
                print(f"Please input an integer between {min_bound} and {max_bound}.")
        except ValueError:
            print(f"Invalid input. Please input an integer between {min_bound} and {max_bound}.")


DEFAULT_DATETIME_FORMAT = "%Y-%m-%d_%H-%M-%S"


class SafeFormatter(string.Formatter):
    def __init__(self, values: dict):
        self.values = values

    def get_value(self, key, args, kwargs):
        # Handle missing keys gracefully
        if isinstance(key, str):
            return self.values.get(key, f"{{{key}}}")
        return super().get_value(key, args, kwargs)

    def format_field(self, value, format_spec):
        # Handle datetime formatting with or without format_spec
        if isinstance(value, datetime.datetime):
            if format_spec:
                return value.strftime(format_spec)
            else:
                return value.strftime(DEFAULT_DATETIME_FORMAT)
        return super().format_field(value, format_spec)


def parse_filename_template(index: int, url: str, template: str) -> str:
    """
    Fill a filename template using metadata, with support for default and custom datetime formats.
    :param index:
    :param url:
    :param template:
    :return:
    """

    placeholders = {
        "index": index,
        "author": extract_video_author(url),
        "id": extract_video_id(url),
        "cdate": datetime.datetime.now()
    }

    formatter = SafeFormatter(placeholders)
    return formatter.format(template, **placeholders)
