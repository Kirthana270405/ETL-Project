import pandas as pd
import json
import os
import warnings
warnings.filterwarnings("ignore", category=UserWarning, message="Could not infer format")

def load_and_clean_data(data_path):
    ext = os.path.splitext(data_path)[1].lower()
    if ext == ".csv":
        df = pd.read_csv(data_path)
    elif ext in [".xlsx", ".xls"]:
        df = pd.read_excel(data_path, engine='openpyxl')
    else:
        raise ValueError("Unsupported file format")
    validation_report = {
        "initial_nulls": int(df.isnull().sum().sum()),
        "columns_checked": [],
        "completeness_passed": False,
        "accuracy_issues": [],
        "consistency_notes": []
    }
    for col in df.columns:
        nulls_before = int(df[col].isnull().sum())
        if nulls_before > 0:
            if pd.api.types.is_numeric_dtype(df[col]):
                df[col] = df[col].fillna(df[col].mean())
            elif pd.api.types.is_datetime64_any_dtype(df[col]):
                mode_val = df[col].mode()
                if not mode_val.empty:
                    df[col] = df[col].fillna(mode_val[0])
            else:
                try:
                    df[col] = pd.to_datetime(df[col])
                    mode_val = df[col].mode()
                    if not mode_val.empty:
                        df[col] = df[col].fillna(mode_val[0])
                except:
                    df[col] = df[col].fillna("Unknown")

        validation_report["columns_checked"].append(col)
        # Accuracy check
        if pd.api.types.is_numeric_dtype(df[col]):
            if not pd.to_numeric(df[col], errors='coerce').notnull().all():
                validation_report["accuracy_issues"].append(f"{col} has non-numeric values")
        if "date" in col.lower():
            try:
                pd.to_datetime(df[col])
            except:
                validation_report["accuracy_issues"].append(f"{col} contains invalid dates")
        # Consistency check
        if df[col].dtype == "object" and df[col].nunique() < 10:
            validation_report["consistency_notes"].append(
                f"{col} has limited unique values: {list(df[col].unique())}"
            )
    remaining_nulls = int(df.isnull().sum().sum())
    validation_report["remaining_nulls"] = remaining_nulls
    validation_report["completeness_passed"] = remaining_nulls == 0
    if remaining_nulls == 0:
        print("Dataset successfully cleaned. No missing values remain.")
    else:
        print(f"Dataset cleaned partially. {remaining_nulls} missing values still remain.")
    validation_path = os.path.join("outputs", "results", "validation_report.json")
    os.makedirs(os.path.dirname(validation_path), exist_ok=True)
    with open(validation_path, "w") as vr:
        json.dump(validation_report, vr, indent=4)
    return df





#dont remove the columns and the data should be modified if nulls, outliers etc.,