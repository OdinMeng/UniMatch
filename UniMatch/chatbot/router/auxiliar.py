import json
import os

# Define the base directory for file operations
BASE_DIR = os.path.dirname(__file__)


def add_message(new_item, file_name):
    """Add a single message to a JSON file, assigning it a unique ID.

    Args:
        new_item: The message to add, provided as a dictionary.
        file_name: The name of the JSON file to store the messages.
    """
    try:
        file_path = os.path.join(BASE_DIR, file_name)

        # Check if the file exists
        if not os.path.exists(file_path):
            # Assign an initial ID when creating a new file
            new_item["Id"] = 1
            data = [new_item]

            # Write the data to a new file
            with open(file_path, "w") as file:
                json.dump(data, file, indent=4)
        else:
            # Load existing messages from the file
            with open(file_path, "r") as file:
                data = json.load(file)

            # Determine the next ID based on existing data
            if data:
                max_id = max(item.get("Id", 0) for item in data)
                new_item["Id"] = max_id + 1
            else:
                new_item["Id"] = 1  # Start from ID 1 if the file is empty

            # Add the new message to the list
            data.append(new_item)

            # Save the updated list back to the file
            with open(file_path, "w") as file:
                json.dump(data, file, indent=4)

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from file {file_name}: {e}")
        raise
    except (IOError, OSError) as e:
        print(f"Error accessing or writing to file {file_name}: {e}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise


def add_messages(new_items, file_name):
    """Add multiple messages to a JSON file, assigning unique IDs to each.

    Args:
        new_items: A list of dictionaries representing the messages to add.
        file_name: The name of the JSON file to store the messages.
    """
    try:
        file_path = os.path.join(BASE_DIR, file_name)

        # Check if the file exists
        if not os.path.exists(file_path):
            # Assign sequential IDs starting from 1 for a new file
            for i, item in enumerate(new_items, 1):
                item["Id"] = i

            # Write all new items to a new file
            with open(file_path, "w") as file:
                json.dump(new_items, file, indent=4)
        else:
            # Load existing messages from the file
            with open(file_path, "r") as file:
                data = json.load(file)

            # Determine the starting ID for the new items
            if data:
                max_id = max(item.get("Id", 0) for item in data)
            else:
                max_id = 0  # Start from ID 1 if the file is empty

            # Assign unique IDs to each new item
            for new_item in new_items:
                max_id += 1
                new_item["Id"] = max_id

            # Add the new items to the existing data
            data.extend(new_items)

            # Save the updated data back to the file
            with open(file_path, "w") as file:
                json.dump(data, file, indent=4)

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from file {file_path}: {e}")
        raise
    except (IOError, OSError) as e:
        print(f"Error accessing or writing to file {file_path}: {e}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise
