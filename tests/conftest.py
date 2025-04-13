# tests/conftest.py
# This file defines Pytest fixtures to set up a Flask app, test client, and sample CSV for testing the data visualization dashboard.

import pytest
import os
import pandas as pd
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app as flask_app

@pytest.fixture
def app():
    """Create and configure a Flask app for testing."""
    flask_app.config.update({
        "TESTING": True,
        "UPLOAD_FOLDER": "test_uploads",
        "SECRET_KEY": "test-secret-key"
    })
    
    # Create test uploads folder
    os.makedirs(flask_app.config["UPLOAD_FOLDER"], exist_ok=True)
    yield flask_app
    
    # Clean up
    for file in os.listdir(flask_app.config["UPLOAD_FOLDER"]):
        os.remove(os.path.join(flask_app.config["UPLOAD_FOLDER"], file))
    os.rmdir(flask_app.config["UPLOAD_FOLDER"])

@pytest.fixture
def client(app):
    """Provide a test client for the Flask app."""
    return app.test_client()

@pytest.fixture
def sample_csv(app):
    """Create a sample CSV file for testing."""
    csv_path = os.path.join(app.config["UPLOAD_FOLDER"], "sample.csv")
    data = {
        "name": ["Alice", "Bob", "Charlie"],
        "age": [25, 30, 35],
        "salary": [50000, 60000, 75000]
    }
    df = pd.DataFrame(data)
    df.to_csv(csv_path, index=False)
    yield csv_path