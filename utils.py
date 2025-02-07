def select_from_choices(prompt: str, choices: list, allow_multiple: bool = True) -> list:
    selected = []

    # Display choices
    def display_choices():
        for i, choice in enumerate(choices, start=1):
            print(f"({i}) {choice}")

    while True:
        if not allow_multiple and len(selected) >= 1:
            break  # Stop if only single selection is allowed and already selected one item

        print(f"Selected items: {', '.join(selected)}" if selected else '', end='\n' if selected else '')
        display_choices()

        # Get valid user inputx
        try:
            user_choice = get_int(f"{prompt} (or press 0 to finish): ", 0, len(choices))
            print()

            if user_choice == 0:
                if allow_multiple:  # If multiple selections allowed, break out only when user opts to finish
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
    while True:
        try:
            user_input = int(input(prompt))
            if min_bound <= user_input <= max_bound:
                return user_input
            else:
                print(f"Please input an integer between {min_bound} and {max_bound}.")
        except ValueError:
            print(f"Invalid input. Please input an integer between {min_bound} and {max_bound}.")
