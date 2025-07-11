import pandas as pd
import numpy as np
import os
def load_metadata(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.csv':
        df = pd.read_csv(file_path)
    elif ext in ['.xlsx', '.xls']:
        df = pd.read_excel(file_path, engine='openpyxl')
    else:
        raise ValueError("Unsupported file format: only .csv and .xlsx are supported")
    metadata = {
        "file_name": os.path.basename(file_path),
        "file_type": ext.replace('.', ''),
        "file_size_kb": round(os.path.getsize(file_path) / 1024, 2),
        "row_count": int(df.shape[0]),
        "column_count": int(df.shape[1]),
        "columns": {}
    }
    for col in df.columns:
        series = df[col]
        stats = {
            "dtype": str(series.dtype),
            "null_count": int(series.isnull().sum())
        }
        if pd.api.types.is_numeric_dtype(series):
            clean_series = series.dropna()
            q1 = clean_series.quantile(0.25)
            q3 = clean_series.quantile(0.75)
            iqr = q3 - q1
            outliers = clean_series[(clean_series < (q1 - 1.5 * iqr)) | (clean_series > (q3 + 1.5 * iqr))]
            stats.update({
                "mean": float(clean_series.mean()) if not clean_series.empty else None,
                "median": float(clean_series.median()) if not clean_series.empty else None,
                "std_dev": float(clean_series.std()) if not clean_series.empty else None,
                "min": float(clean_series.min()) if not clean_series.empty else None,
                "max": float(clean_series.max()) if not clean_series.empty else None,
                "kurtosis": float(clean_series.kurt()) if not clean_series.empty else None,
                "skewness": float(clean_series.skew()) if not clean_series.empty else None,
                "outliers_count": int(outliers.count())
            })
        metadata["columns"][col] = stats
    return metadata



