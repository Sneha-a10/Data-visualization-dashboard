# tests/test_utils.py
# This file contains Pytest tests for utility functions in the Flask data visualization dashboard.

import pytest
import os
from app import cleanup_files

def test_cleanup_files(app):
    """Test the cleanup_files function."""
    # Create a dummy file
    dummy_file = os.path.join(app.config["UPLOAD_FOLDER"], "dummy.txt")
    with open(dummy_file, "w") as f:
        f.write("test")

    assert os.path.exists(dummy_file)
    cleanup_files(app.config["UPLOAD_FOLDER"])
    assert not os.path.exists(dummy_file)