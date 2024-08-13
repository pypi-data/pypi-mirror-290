import os
import json


def load_config(path="config.json") -> dict:
    """Load a JSON config file from the given path.

    Args:
        path (str, optional): The path to the config file. Defaults to "config.json".

    Raises:
        FileNotFoundError: If the file is not found at the given path.
        ValueError: If the file is not valid JSON.

    Returns:
        dict: The config file as a dictionary
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Config file not found at {path}")

    try:
        with open(path, "r") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in config file: {e}")
