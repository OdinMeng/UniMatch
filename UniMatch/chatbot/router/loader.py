import os

from semantic_router import RouteLayer

FILENAME = "layer.json"
BASE_DIR = os.path.dirname(__file__)
FILE_PATH = os.path.join(BASE_DIR, FILENAME)


def load_intention_classifier() -> RouteLayer:
    """
    Load json a file in the `router` folder.

    Returns:
        RouteLayer object to classify user intentions.

    Raises:
        ValueError: If the file type is not supported.

    """
    if not os.path.exists(FILE_PATH):
        raise FileNotFoundError(f"File not found: {FILE_PATH}")

    rl = RouteLayer.from_json(FILE_PATH)

    return rl
