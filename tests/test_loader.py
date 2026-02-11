import unittest
import pandas as pd
import os
import sys

# Add src to path so we can import data_loader
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from data_loader import load_and_process_data


class TestDataLoader(unittest.TestCase):
    def setUp(self):
        # Create a dummy CSV for testing
        self.test_csv = "test_data.csv"
        df = pd.DataFrame(
            {
                "Date": ["2020-01-01", "2020-01-02", "2020-01-03"],
                "Price": [50.0, 52.0, 51.0],
            }
        )
        df.to_csv(self.test_csv, index=False)

    def tearDown(self):
        # Clean up
        if os.path.exists(self.test_csv):
            os.remove(self.test_csv)

    def test_load_data_success(self):
        """Test that data loads correctly."""
        df = load_and_process_data(self.test_csv, start_date="2020-01-01")
        self.assertEqual(len(df), 3)
        self.assertIn("Date", df.columns)
        self.assertIn("Price", df.columns)

    def test_file_not_found(self):
        """Test that it raises FileNotFoundError for bad paths."""
        with self.assertRaises(FileNotFoundError):
            load_and_process_data("non_existent.csv")


if __name__ == "__main__":
    unittest.main()
