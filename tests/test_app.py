# Standard library imports
import json

# Third party imports
import pytest
import requests
from flask import request
from werkzeug.wrappers import Response

# Local application imports
from app.main import the_app
from app.models import Order, Seats
from app.utilities import parse_flask_response, parse_requests_response


# Add end-point for application for testing
@the_app.route("/client-info", methods=["GET"])
def get_client_info():
    """Additional end-point to extract URL that the application is running at.

    References:
        https://fastapi.tiangolo.com/advanced/using-request-directly/#use-the-request-object-directly
    """
    host = f"{request.scheme}://{request.remote_addr}"
    port = request.environ["SERVER_PORT"]

    info = {
        "host": host,
        "port": port
    }

    return info


class Useful:
    """Useful fixtures."""

    @pytest.fixture
    def testclient(self):
        """Test client."""
        with the_app.test_client() as client:

            yield client

    @pytest.fixture
    def url(self, testclient):
        """URL of the test client (to use for requests)."""
        response = testclient.get("/client-info")

        response = parse_flask_response(response=response)

        url = f"http://{response['host']}:{response['port']}"

        return url

    @pytest.fixture
    def headers(self):
        """Headers."""
        return {"Content-Type":"application/json"}

    def test_root_via_requests(self, testclient, headers):
        """Test welcome endpoint using requests."""
        # URL as defined in ./vscode/launch.json, NOT app/main.py
        url = "http://127.0.0.1:8000"

        try:
            response = requests.get(f"{url}", headers=headers)
        except requests.exceptions.ConnectionError:
            pytest.skip(
                "test_root_via_requests requires the application to be running"
                ". For Visual Studio Code users, use 'Run and Debug'")

        # Note how the response is a different type here as we're sending
        # a request via the requests package.
        assert isinstance(response, requests.models.Response)

        actual = parse_requests_response(response=response)

        expected = {"message": "Welcome to our restaurant"}

        assert actual == expected

    def test_root_via_client(self, testclient, headers):
        """Test welcome endpoint via the test client."""
        response = testclient.get("/", headers=headers)

        assert isinstance(response, Response)

        actual = parse_flask_response(response=response)

        expected = {"message": "Welcome to our restaurant"}

        assert actual == expected


@pytest.mark.usefixtures("testclient", "headers", "url")
class TestApp(Useful):
    """Test the application."""

    @pytest.mark.parametrize("name", [None, "Aaa", "bbb", "ccc"])
    def test_find_waiter(self, testclient, headers, name):
        """Test waiter."""
        if name is None:
            expected_msg = "Hello, I'm your waiter for today."
            url = "/waiter"
        else:
            expected_msg = f"Hello, I'm {name.title()}, your waiter for today."
            url = f"/waiter/{name}"

        expected = {"message": expected_msg}

        response = testclient.post(url, headers=headers)

        assert isinstance(response, Response)

        actual = parse_flask_response(response=response)

        assert actual == expected

    @pytest.mark.parametrize("n_seats", [1, 3, 4])
    def test_find_table(self, testclient, headers, n_seats):
        """Test the table endpoint."""
        data = Seats(seats=n_seats).to_dict()

        response = testclient.post(
            "/table",
            data=json.dumps(data),
            headers=headers,
        )

        assert isinstance(response, Response)

        actual = parse_flask_response(response=response)

        expected = {"Table number": 100 + int(n_seats)}

        assert actual == expected

    @pytest.mark.parametrize("n_seats", [-2, 0, 0.9, 2.3])
    def test_find_table_error(self, testclient, headers, n_seats):
        """Test the table endpoint with invalid inputs.

        Extended Summary:
            Check that an error is raised when requesting <1 seats.
        """
        with pytest.raises(ValueError):

            Seats(seats=n_seats).to_dict()

    @pytest.mark.parametrize("use_pydantic", [True, False])
    def test_order(self, testclient, headers, use_pydantic):
        """Test the order endpoint."""
        if use_pydantic:
            order = Order(food="Salmon").to_dict()

        else:
            order = {"food": "Salmon"}

        response = testclient.post(
            "/order",
            data=json.dumps(order),
            headers=headers,
        )

        assert isinstance(response, Response)

        actual = parse_flask_response(response=response)

        expected = {
            "Food in its way": "Salmon",
            "Drinks on their way": None,
        }

        assert actual == expected
