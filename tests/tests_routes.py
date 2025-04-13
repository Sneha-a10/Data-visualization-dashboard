# tests/test_routes.py
# This file contains Pytest tests for all routes in the Flask data visualization dashboard, including success cases and edge cases.

import pytest
import os
from werkzeug.datastructures import FileStorage

def test_index(client):
    """Test the index route."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"DATA VISUALIZATION BOARD" in response.data

def test_upload_file_success(client, sample_csv):
    """Test successful file upload."""
    with open(sample_csv, "rb") as f:
        data = {"file": (FileStorage(f, "sample.csv"), "sample.csv")}
        response = client.post("/upload", data=data, content_type="multipart/form-data")
        assert response.status_code == 200
        assert b"sample" in response.data  # Table name
        assert b"name,age,salary" in response.data  # Column names

def test_upload_no_file(client):
    """Test upload with no file."""
    response = client.post("/upload", content_type="multipart/form-data")
    assert response.status_code == 200  # Returns index with error message
    assert b"No file part" in response.data

def test_upload_empty_filename(client):
    """Test upload with empty filename."""
    data = {"file": (FileStorage(None, ""), "")}
    response = client.post("/upload", data=data, content_type="multipart/form-data")
    assert response.status_code == 200
    assert b"No file selected" in response.data

def test_generate_graph_bar(client, sample_csv):
    """Test generating a bar graph."""
    # First, upload the file
    with open(sample_csv, "rb") as f:
        data = {"file": (FileStorage(f, "sample.csv"), "sample.csv")}
        client.post("/upload", data=data, content_type="multipart/form-data")

    # Generate graph
    data = {
        "graph_type": "bar",
        "filename": "sample.csv",
        "x_column": "name",
        "y_column": "age",
        "graph_color": "#4fb5c5"
    }
    response = client.post("/generate-graph", data=data)
    assert response.status_code == 200
    assert b"data:image/png;base64" in response.data  # Graph image
    assert os.path.exists(os.path.join("test_uploads", "graph_sample.png"))

def test_generate_graph_invalid_file(client):
    """Test graph generation with missing file."""
    data = {
        "graph_type": "bar",
        "filename": "nonexistent.csv",
        "x_column": "name",
        "y_column": "age",
        "graph_color": "#4fb5c5"
    }
    response = client.post("/generate-graph", data=data)
    assert response.status_code == 200
    assert b"File not found. Please upload again." in response.data

def test_generate_graph_no_graph_type(client, sample_csv):
    """Test graph generation without graph type."""
    with open(sample_csv, "rb") as f:
        data = {"file": (FileStorage(f, "sample.csv"), "sample.csv")}
        client.post("/upload", data=data, content_type="multipart/form-data")

    data = {
        "filename": "sample.csv",
        "x_column": "name",
        "y_column": "age",
        "graph_color": "#4fb5c5"
    }
    response = client.post("/generate-graph", data=data)
    assert response.status_code == 302  # Redirects to index
    # Follow redirect to check flash message
    response = client.get(response.headers["Location"])
    assert b"Please select a graph type." in response.data

def test_generate_graph_heatmap_no_numeric(client, app):
    """Test heatmap with non-numeric data."""
    csv_path = os.path.join(app.config["UPLOAD_FOLDER"], "non_numeric.csv")
    data = {"category": ["A", "B", "C"]}
    pd.DataFrame(data).to_csv(csv_path, index=False)

    with open(csv_path, "rb") as f:
        data = {"file": (FileStorage(f, "non_numeric.csv"), "non_numeric.csv")}
        client.post("/upload", data=data, content_type="multipart/form-data")

    data = {
        "graph_type": "heatmap",
        "filename": "non_numeric.csv",
        "graph_color": "#4fb5c5"
    }
    response = client.post("/generate-graph", data=data)
    assert response.status_code == 302  # Redirects to index
    response = client.get(response.headers["Location"])
    assert b"Heatmap requires at least 2 numeric columns." in response.data

def test_download_graph_success(client, sample_csv):
    """Test downloading a generated graph."""
    # Upload and generate graph
    with open(sample_csv, "rb") as f:
        data = {"file": (FileStorage(f, "sample.csv"), "sample.csv")}
        client.post("/upload", data=data, content_type="multipart/form-data")

    data = {
        "graph_type": "bar",
        "filename": "sample.csv",
        "x_column": "name",
        "y_column": "age",
        "graph_color": "#4fb5c5"
    }
    client.post("/generate-graph", data=data)

    response = client.get("/download-graph/graph_sample.png")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "image/png"

def test_download_graph_not_found(client):
    """Test downloading a non-existent graph."""
    response = client.get("/download-graph/nonexistent.png")
    assert response.status_code == 200
    assert b"Graph file not found." in response.data

def test_about_graphs(client):
    """Test the about_graphs route."""
    response = client.get("/about_graphs")
    assert response.status_code == 200
    assert b"About Graphs" in response.data