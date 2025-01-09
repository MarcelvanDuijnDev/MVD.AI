import json
import re

# Path to the filters JSON file
FILTERS_FILE = "filters.json"

# Load filters from JSON file
def load_filters():
    """Load filter settings from the filters.json file."""
    with open(FILTERS_FILE, "r") as file:
        return json.load(file)

# Save updated filters to JSON file
def save_filters(filters):
    """Save updated filter settings to the filters.json file."""
    with open(FILTERS_FILE, "w") as file:
        json.dump(filters, file, indent=4)

# Check if a message is allowed
def is_message_allowed(message):
    """
    Check if a message passes the filters.
    Args:
        message (str): The message to be checked.
    Returns:
        tuple: (is_allowed (bool), reason (str))
    """
    filters = load_filters()
    if not filters["enabled"]:
        return True, "Filtering is disabled"

    # Check categories
    for category, details in filters["categories"].items():
        if details["enabled"]:
            for word in details["words"]:
                if word in message.lower():
                    return False, f"Blocked by {category} filter: {word}"

    # Check patterns
    for pattern in filters["patterns"]:
        if pattern["enabled"]:
            if re.search(pattern["pattern"], message):
                return False, f"Blocked by pattern filter: {pattern['name']}"

    return True, "Message is allowed"

# Update filters dynamically
def update_filters(update_data):
    """
    Update filters dynamically.
    Args:
        update_data (dict): Contains the updated settings.
    Returns:
        dict: Updated filter settings.
    """
    filters = load_filters()
    filters.update(update_data)
    save_filters(filters)
    return filters

# Manage filter categories and patterns
def manage_filters(update=None):
    """
    Manage filters by viewing or updating them.
    Args:
        update (dict, optional): Update data to apply. Defaults to None.
    Returns:
        dict: Current or updated filter settings.
    """
    if update:
        return update_filters(update)
    return load_filters()
