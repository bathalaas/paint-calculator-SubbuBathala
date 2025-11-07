# tests/test_api.py

import pytest
import math
from paint_calculator.api import (
    calculate_feet,
    calculate_gallons_required,
    sanitize_input,
    api
)
from flask import Flask


@pytest.fixture
def client():
    """Create a Flask test client for API testing."""
    app = Flask(__name__)
    app.register_blueprint(api)
    with app.test_client() as client:
        yield client


# -----------------------------
# Unit Tests for Helper Functions
# -----------------------------

def test_calculate_feet_valid():
    data = {"length": 10, "width": 12, "height": 8}
    result = calculate_feet(data)
    assert result == 960, "Feet calculation should multiply all dimensions"


def test_calculate_feet_invalid_key():
    data = {"length": 10, "height": 8}
    with pytest.raises(KeyError):
        calculate_feet(data)


def test_calculate_gallons_required_small_area():
    result = calculate_gallons_required({"ft": 100})
    assert result == 0, "100 sq ft requires 0 gallons when floored"


def test_calculate_gallons_required_large_area():
    result = calculate_gallons_required({"ft": 1000})
    expected = math.floor(1000 / 350)
    assert result == expected


def test_sanitize_input_negative():
    assert sanitize_input(-12) == 12


def test_sanitize_input_string():
    assert sanitize_input("-7") == 7


def test_sanitize_input_float_string():
    with pytest.raises(ValueError):
        sanitize_input("7.5")


# -----------------------------
# Integration Test for API Endpoint
# -----------------------------

def test_calculate_api(client):
    payload = {
        "room1": {"length": 10, "width": 12, "height": 8},
        "room2": {"length": 15, "width": 10, "height": 9}
    }
    response = client.post("/api/v1/calculate", json=payload)
    assert response.status_code == 200

    data = response.get_json()
    assert "total_gallons" in data
    assert data["room1"]["ft"] == 960
    assert isinstance(data["total_gallons"], (int, float))


def test_calculate_api_empty(client):
    response = client.post("/api/v1/calculate", json={})
    assert response.status_code == 200
    data = response.get_json()
    assert data["total_gallons"] == 0
