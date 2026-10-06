import unittest
from pathlib import Path
import tempfile
import pandas as pd
from streamlit.testing.v1 import AppTest
from data import DATA_PATH, load_data

class DashboardTests(unittest.TestCase):
    def test_capacity_and_missing_values(self):
        df = load_data()
        self.assertEqual(df.Additional_Capacity_MPPA.tolist(), [12,18,20,20])
        self.assertEqual(df.Passenger_Capacity_MPPA.max(), 70)
        self.assertTrue(pd.isna(df.Runways.iloc[2]))
        self.assertTrue(pd.isna(df.Area_Hectares.iloc[1]))

    def test_invalid_schema_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "bad.csv"
            path.write_text("Phase\nPhase 1\n")
            with self.assertRaises(ValueError):
                load_data(path)

    def test_dashboard_filters_and_no_overwrite(self):
        before = DATA_PATH.read_bytes()
        at = AppTest.from_file(str(Path(__file__).with_name("app.py"))).run(timeout=30)
        self.assertFalse(at.exception)
        self.assertEqual(at.metric[0].value, "70 MPPA")
        at.multiselect[0].set_value(["Phase 2"]).run()
        self.assertFalse(at.exception)
        self.assertEqual(at.metric[0].value, "30 MPPA")
        self.assertEqual(at.selectbox[0].options, ["Phase 2"])
        self.assertEqual(at.dataframe[0].value.Additional_Capacity_MPPA.tolist(), [18])
        at.multiselect[0].set_value([]).run()
        self.assertFalse(at.exception)
        self.assertTrue(at.warning)
        self.assertEqual(DATA_PATH.read_bytes(), before)

if __name__ == "__main__":
    unittest.main()
