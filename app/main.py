"""The Restaurant application."""

# Standard library imports
import json

# Third party imports
from flask import Flask, request

# Local application imports
from .utilities import parse_flask_response


# Create application
the_app = Flask(__name__)


# Set secret key for app (required for passing data between end-points)
the_app.secret_key = "my-key"


# Define a trivial restauraunt menu
menu = {
    "Starters": {
        "Olives": 4,
        "Bread": 3,
    },
    "Mains": {
        "Margherita": 10,
        "Spaghetti Bolognese": 8,
        "Salmon": 15,
    },
    "Desserts": {
        "Chocolate cake": 5,
        "Waffles And Ice-cream": 4,
    },
    "Drinks": {
        "Tap Water": 0,
        "Sparkling Water": 1,
        "Lemonade": 4,
    }
}


@the_app.route('/', methods=['GET'])
def welcome() -> dict:
    """Welcome.

    Returns:
        dict: Welcome message
    """
    output = {"message": "Welcome to our restaurant"}

    return json.dumps(output)


@the_app.route('/waiter', methods=['POST'])
def find_any_waiter() -> dict:
    """Speak to the waiter.

    Returns:
        dict: Waiter greeting
    """
    output = {"message": "Hello, I'm your waiter for today."}

    return json.dumps(output)


@the_app.route("/waiter/<string:name>", methods=["POST"])
def find_waiter(name: str) -> dict:
    """Speak to a specific waiter.

    Args:
        name (str): Name of waiter

    Returns:
        dict: Waiter greeting

    Extended Summary:
        This uses a path argument as opposed to a query argument.
    """
    waiter = name.title()

    output = {"message": f"Hello, I'm {waiter}, your waiter for today."}

    return json.dumps(output)

@the_app.route('/table', methods=['POST'])
def find_table() -> dict:
    """Ask for a table with a given number of seats.

    Args:
        seats (Seats): Number of seats required

    Returns:
        dict: Table number
    """
    response = parse_flask_response(response=request)

    n_seats = response["seats"]

    output = {"Table number": 100 + n_seats}

    return json.dumps(output)


@the_app.route('/menu', methods=['GET'])
def get_menu() -> dict:
    """Get menu.

    Returns:
        dict: Menu
    """
    return json.dumps(menu)


@the_app.route('/order', methods=['POST'])
def post_order() -> dict:
    """Order item(s) from the menu.

    Args:
        order (Order): Food and/or drink orders.

    Returns:
        dict: Order confirmation
    """
    response = parse_flask_response(response=request)

    food = response.get("food", None)
    drinks = response.get("drink", None)

    output = {
        "Food in its way": food,
        "Drinks on their way": drinks,
    }

    return json.dumps(output)


if __name__ == "__main__":

    # This line is not used in ' Run and Debug' mode
    the_app.run(debug=True, host="127.0.0.1", port=5000)
