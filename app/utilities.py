"""Useful utility functions."""

# Standard library imports
import json

# Third party library imports
import requests
from werkzeug.wrappers import Response

# Local application imports
# n/a


def parse_flask_response(response: Response) -> dict:
    """Parse a Flask client request.

    Args:
        response (Response): Response from a Flask client request.

    Returns:
        dict: Response as dictionary
    """
    return dict(json.loads(response.data))

def parse_requests_response(response: requests.models.Response) -> dict:
    """Parse a requests request.

    Args:
        response (requests.models.Response): Response from a requests request.

    Returns:
        dict: Response as dictionary
    """
    return response.json()
