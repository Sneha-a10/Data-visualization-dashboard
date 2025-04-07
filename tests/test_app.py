import unittest
import os
import pandas as pd
from flask import Flask
from app import app  

class AppTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['UPLOAD_FOLDER'] = 'test_uploads'  # Create a test upload folder
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
        self.app = app.test_client()

        # Create a sample CSV file for testing
        self.sample_csv_path = os.path.join(app.config['UPLOAD_FOLDER'], 'sample.csv')
        sample_data = {'col1': [1, 2], 'col2': [3, 4]}
        df = pd.DataFrame(sample_data)
        df.to_csv(self.sample_csv_path, index=False)

    def tearDown(self):
        # Clean up the test upload folder and file
        for file in os.listdir(app.config['UPLOAD_FOLDER']):
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file))
        os.rmdir(app.config['UPLOAD_FOLDER'])

    def test_upload_file(self):
        with open(self.sample_csv_path, 'rb') as f:
            data = {'file': (f, 'sample.csv')}
            response = self.app.post('/upload', data=data, content_type='multipart/form-data')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'sample.csv', response.data)  # Check if filename is in response

    def test_generate_graph(self):
        with open(self.sample_csv_path, 'rb') as f:
            data = {'file': (f, 'sample.csv')}
            self.app.post('/upload', data=data, content_type='multipart/form-data')

        data = {
            'graph_type': 'bar',
            'filename': 'sample.csv',
            'x_column': 'col1',
            'y_column': 'col2',
            'graph_color': '#000000'
        }
        response = self.app.post('/generate-graph', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<img src="data:image/png;base64', response.data)  # Check if graph is in response

if __name__ == '__main__':
    unittest.main()
