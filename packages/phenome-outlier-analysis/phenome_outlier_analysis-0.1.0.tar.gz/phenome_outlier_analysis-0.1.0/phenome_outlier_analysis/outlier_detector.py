"""
outlier_detection.py

This module provides a class for outlier detection in datasets using various normalization methods.
It supports context-specific and global outlier detection strategies.
"""

import logging

import numpy as np
import pandas as pd
from scipy.stats import zscore
from tqdm import tqdm

# Set up basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OutlierDetector:
    def __init__(self, df, analyte_columns, segment_columns=['sex']):
        """
        Initialize the OutlierDetector with a DataFrame and column specifications.

        Args:
            df (pd.DataFrame): Input DataFrame.
            analyte_columns (list): List of columns to analyze for outliers.
            segment_columns (list): List of columns to use for segmentation.
        """
        self.df = df
        self.analyte_columns = analyte_columns
        self.segment_columns = segment_columns
        self.global_lower_cutoff = None
        self.global_upper_cutoff = None

    def calculate_double_mad(self, series, take_log=False):
        """Calculate left and right Median Absolute Deviations (MADs) from the median."""
        clean_series = series.dropna()
        if take_log:
            clean_series = np.log1p(clean_series[clean_series > 0])
        
        median = clean_series.median()
        abs_deviation = (clean_series - median).abs()
        
        n = len(clean_series)
        mid = n // 2
        
        if n % 2 == 0:  # Even number of elements
            left_mad = abs_deviation.iloc[:mid].median()
            right_mad = abs_deviation.iloc[mid:].median()
        else:  # Odd number of elements
            left_mad = abs_deviation.iloc[:mid+1].median()
            right_mad = abs_deviation.iloc[mid:].median()
        
        if left_mad == 0:
            logger.warning("Left MAD is 0, indicating no variability for lower half of values.")
        if right_mad == 0:
            logger.warning("Right MAD is 0, indicating no variability for upper half of values.")
        
        return left_mad, right_mad

    def normalize_series(self, series, method='double_mad'):
        """Normalize a series using the specified method."""
        if method == 'double_mad':
            left_mad, right_mad = self.calculate_double_mad(series)
            median = series.dropna().median()
            mad_series = pd.Series(left_mad, index=series.index)
            mad_series[series > median] = right_mad
            
            normalized = (series - median).abs() / mad_series
            normalized[series == median] = 0
            normalized[series < median] *= -1
        elif method == 'zscore':
            normalized = zscore(series)
        else:
            raise ValueError(f"Unsupported normalization method: {method}")
        
        return normalized

    def calculate_percentile_cutoffs(self, df, columns, lower_percentile=0.01, upper_percentile=0.99):
        """Calculate global percentile cutoffs based on the specified columns of a DataFrame."""
        combined = pd.concat([df[col] for col in columns])
        return combined.quantile(lower_percentile), combined.quantile(upper_percentile)

    def create_binary_matrix(self, df, columns, lower_cutoff, upper_cutoff):
        """Create a binary matrix indicating outliers based on specified cutoffs."""
        return pd.DataFrame({col: ((df[col] < lower_cutoff) | (df[col] > upper_cutoff)).astype(int) for col in columns})

    def normalize_dataframe(self, df, columns, method='double_mad', take_log=False):
        """Normalize specified columns in a DataFrame."""
        df_normalized = df.copy()
        for col in columns:
            series = np.log1p(df[col]) if take_log else df[col]
            df_normalized[col] = self.normalize_series(series, method)
        return df_normalized

    def detect_outliers(self, df, columns, lower_cutoff, upper_cutoff):
        """Detect outliers in the specified columns of a DataFrame."""
        binary_matrix = self.create_binary_matrix(df, columns, lower_cutoff, upper_cutoff)
        return {
            'adjusted_df': df,
            'binary_matrix': binary_matrix,
            'lower_cutoff': lower_cutoff,
            'upper_cutoff': upper_cutoff
        }

    def context_specific_outlier_detection(self, method='double_mad', take_log=False):
        """Perform context-specific outlier detection by segmenting the DataFrame."""
        results = {}
        for column in self.segment_columns:
            for value in tqdm(self.df[column].dropna().unique(), desc=f"Processing {column}"):
                segment_df = self.df[self.df[column] == value].copy()
                segment_df = self.normalize_dataframe(segment_df, self.analyte_columns, method, take_log)
                results[(column, value)] = self.detect_outliers(segment_df, self.analyte_columns, self.global_lower_cutoff, self.global_upper_cutoff)
        return results

    def super_global_outlier_detection(self, method='double_mad', take_log=False):
        """Evaluate outliers on a global scale."""
        df_global = self.normalize_dataframe(self.df, self.analyte_columns, method, take_log)
        return {('global', 'global'): self.detect_outliers(df_global, self.analyte_columns, self.global_lower_cutoff, self.global_upper_cutoff)}

    def get_global_cutoffs(self, lower_percentile=0.01, upper_percentile=0.99, method='double_mad', take_log=False):
        """Get global cutoffs for outlier detection."""
        df_normalized = self.normalize_dataframe(self.df, self.analyte_columns, method, take_log)
        self.global_lower_cutoff, self.global_upper_cutoff = self.calculate_percentile_cutoffs(
            df_normalized, self.analyte_columns, lower_percentile, upper_percentile
        )
        logger.info(f"Global lower cutoff: {self.global_lower_cutoff}")
        logger.info(f"Global upper cutoff: {self.global_upper_cutoff}")

    def perform_outlier_detection(self, lower_percentile=0.01, upper_percentile=0.99, method='double_mad', take_log=False):
        """
        Perform outlier detection on the given DataFrame.

        Args:
            lower_percentile (float): Lower percentile for cutoff calculation.
            upper_percentile (float): Upper percentile for cutoff calculation.
            method (str): Normalization method ('double_mad' or 'zscore').
            take_log (bool): Whether to apply log transformation before normalization.

        Returns:
            tuple: Context-specific results and super-global results.
        """
        self.get_global_cutoffs(lower_percentile, upper_percentile, method, take_log)

        results_context_specific = self.context_specific_outlier_detection(method, take_log)
        results_super_global = self.super_global_outlier_detection(method, take_log)

        return results_context_specific, results_super_global