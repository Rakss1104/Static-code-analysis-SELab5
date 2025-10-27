"""
Simple inventory management system.

This module provides basic functions to manage a stock inventory,
including adding, removing, and querying items.
"""

import json
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def add_item(stock_data, item="default", qty=0, logs=None):
    """
    Adds a specified quantity of an item to the stock.

    Args:
        stock_data (dict): The inventory dictionary.
        item (str): The name of the item to add.
        qty (int): The quantity to add.
        logs (list, optional): A list to append log messages to. Defaults to None.
    """
    if logs is None:
        logs = []  # Fix for dangerous default value

    if not item:
        logging.warning("No item name provided. Skipping.")
        return

    # Basic type checking (from original code's comment)
    if not isinstance(qty, int):
        # Use lazy % formatting for logging
        logging.error("Invalid quantity '%s' for item '%s'. Must be an integer.", qty, item)
        return

    stock_data[item] = stock_data.get(item, 0) + qty
    log_msg = f"Added {qty} of {item}"  # f-string is fine here as it's used twice
    logs.append(f"{datetime.now()}: {log_msg}")
    # Use lazy % formatting for logging
    logging.info("Added %d of %s", qty, item)


def remove_item(stock_data, item, qty):
    """
    Removes a specified quantity of an item from the stock.

    If the quantity drops to 0 or below, the item is removed.

    Args:
        stock_data (dict): The inventory dictionary.
        item (str): The name of the item to remove.
        qty (int): The quantity to remove.
    """
    try:
        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]
            # Use lazy % formatting for logging
            logging.info("Removed item '%s' from stock (quantity was <= 0).", item)
    except KeyError:
        # Specific exception instead of bare 'except'
        # Use lazy % formatting for logging
        logging.warning("Failed to remove item '%s': Item not found in stock.", item)
    except TypeError:
        # Use lazy % formatting for logging
        logging.error("Failed to remove item '%s': Invalid quantity or stock value.", item)


def get_qty(stock_data, item):
    """
    Gets the current quantity of a specific item.

    Args:
        stock_data (dict): The inventory dictionary.
        item (str): The name of the item to query.

    Returns:
        int: The quantity of the item, or 0 if not found.
    """
    return stock_data.get(item, 0)


def load_data(file="inventory.json"):
    """
    Loads the inventory data from a JSON file.

    Args:
        file (str, optional): The filename to load from. Defaults to "inventory.json".

    Returns:
        dict: The loaded inventory data.
    """
    try:
        # Use 'with' for safe file handling and specify encoding
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Use lazy % formatting for logging
            logging.info("Data loaded successfully from %s.", file)
            return data
    except FileNotFoundError:
        # Use lazy % formatting for logging
        logging.warning("Data file '%s' not found. Starting with empty inventory.", file)
        return {}
    except json.JSONDecodeError:
        # Use lazy % formatting for logging
        logging.error("Could not decode JSON from '%s'. Starting with empty inventory.", file)
        return {}


def save_data(stock_data, file="inventory.json"):
    """
    Saves the inventory data to a JSON file.

    Args:
        stock_data (dict): The inventory dictionary to save.
        file (str, optional): The filename to save to. Defaults to "inventory.json".
    """
    try:
        # Use 'with' for safe file handling and specify encoding
        with open(file, "w", encoding="utf-8") as f:
            json.dump(stock_data, f, indent=4)
            # Use lazy % formatting for logging
            logging.info("Data saved successfully to %s.", file)
    except IOError as e:
        # Use lazy % formatting for logging
        logging.error("Could not write to file '%s': %s", file, e)


def print_data(stock_data):
    """
    Prints a formatted report of all items in stock.

    Args:
        stock_data (dict): The inventory dictionary.
    """
    print("\n--- Items Report ---")
    if not stock_data:
        print("Inventory is empty.")
    else:
        for item, qty in stock_data.items():
            print(f"{item}: {qty}")  # f-strings are fine for print()
    print("--------------------\n")


def check_low_items(stock_data, threshold=5):
    """
    Finds all items at or below a given stock threshold.

    Args:
        stock_data (dict): The inventory dictionary.
        threshold (int, optional): The low-stock threshold. Defaults to 5.

    Returns:
        list: A list of item names that are low in stock.
    """
    result = []
    for item, qty in stock_data.items():
        if qty <= threshold:
            result.append(item)
    return result


def main():
    """
    Main function to run the inventory management script.
    """
    # Load data first, or start with an empty dict
    stock = load_data()
    action_logs = []

    add_item(stock, "apple", 10, action_logs)
    add_item(stock, "banana", 15, action_logs)

    # This will now fail gracefully and log an error
    add_item(stock, 123, "ten", action_logs)  # invalid types, now checked

    remove_item(stock, "apple", 3)
    remove_item(stock, "orange", 1)  # Will log a warning (item not found)

    print_data(stock)

    print(f"Apple stock: {get_qty(stock, 'apple')}")
    print(f"Low items: {check_low_items(stock, 10)}")

    save_data(stock)

    # This was the dangerous 'eval' call, which is now removed.
    logging.info("Script execution finished.")


# Standard Python entry point
if __name__ == "__main__":
    main()

