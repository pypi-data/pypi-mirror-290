import unittest

import numpy as np
import pandas as pd

from phenome_outlier_analysis import OutlierDetector


class TestOutlierDetector(unittest.TestCase):
    def setUp(self):
        # Create a sample DataFrame for testing
        self.df = pd.DataFrame({
            'analyte1': [1, 2, 3, 4, 5, 100],
            'analyte2': [10, 20, 30, 40, 50, 1000],
            'sex': ['M', 'F', 'M', 'F', 'M', 'F']
        })
        self.analyte_columns = ['analyte1', 'analyte2']
        self.segment_columns = ['sex']
        self.detector = OutlierDetector(self.df, self.analyte_columns, self.segment_columns)

    def test_initialization(self):
        self.assertIsInstance(self.detector, OutlierDetector)
        self.assertEqual(self.detector.analyte_columns, self.analyte_columns)
        self.assertEqual(self.detector.segment_columns, self.segment_columns)

    def test_calculate_double_mad(self):
        # Symmetric case (odd length)
        series1 = pd.Series([1, 2, 3, 4, 5])
        left_mad1, right_mad1 = self.detector.calculate_double_mad(series1)
        self.assertAlmostEqual(left_mad1, right_mad1)

        # Symmetric case (even length)
        series2 = pd.Series([1, 2, 3, 4, 5, 6])
        left_mad2, right_mad2 = self.detector.calculate_double_mad(series2)
        self.assertAlmostEqual(left_mad2, right_mad2)

        # Asymmetric case
        series3 = pd.Series([1, 2, 3, 4, 5, 100, 101, 102])
        left_mad3, right_mad3 = self.detector.calculate_double_mad(series3)
        self.assertGreater(right_mad3, left_mad3)

        # Large dataset case (simulating proteomic data)
        np.random.seed(42)  # for reproducibility
        normal_data = np.random.normal(loc=5, scale=1, size=10000)
        outliers = np.random.normal(loc=15, scale=2, size=100)
        series4 = pd.Series(np.concatenate([normal_data, outliers]))
        left_mad4, right_mad4 = self.detector.calculate_double_mad(series4)
        self.assertGreater(right_mad4, left_mad4)
        
        # Original case (small sample, single outlier)
        # We now expect equal MADs for this case, given our implementation
        series5 = pd.Series([1, 2, 3, 4, 5, 100])
        left_mad5, right_mad5 = self.detector.calculate_double_mad(series5)
        self.assertAlmostEqual(left_mad5, right_mad5)

    def test_normalize_series(self):
        series = pd.Series([1, 2, 3, 4, 5, 100])
        normalized = self.detector.normalize_series(series)
        self.assertEqual(len(normalized), len(series))
        self.assertGreater(abs(normalized.iloc[-1]), abs(normalized.iloc[0]))

    def test_detect_outliers(self):
        self.detector.get_global_cutoffs()
        results = self.detector.detect_outliers(self.df, self.analyte_columns, self.detector.global_lower_cutoff, self.detector.global_upper_cutoff)
        self.assertIn('adjusted_df', results)
        self.assertIn('binary_matrix', results)
        self.assertIn('lower_cutoff', results)
        self.assertIn('upper_cutoff', results)

    def test_context_specific_outlier_detection(self):
        self.detector.get_global_cutoffs()
        results = self.detector.context_specific_outlier_detection()
        self.assertIn(('sex', 'M'), results)
        self.assertIn(('sex', 'F'), results)

    def test_super_global_outlier_detection(self):
        self.detector.get_global_cutoffs()
        results = self.detector.super_global_outlier_detection()
        self.assertIn(('global', 'global'), results)

if __name__ == '__main__':
    unittest.main()