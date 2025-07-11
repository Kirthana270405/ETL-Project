import os
import sys
import json
from glob import glob
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "logic")))
from metadata import load_metadata
from clean import load_and_clean_data
from visualize import generate_visualizations
datasets_path = os.path.abspath("Datasets")
output_base_path = os.path.abspath("outputs/results")
os.makedirs(output_base_path, exist_ok=True)
data_files = glob(os.path.join(datasets_path, "*.csv")) + glob(os.path.join(datasets_path, "*.xlsx"))
if not data_files:
    print("No datasets found in the 'Datasets' folder.")
    sys.exit()
print("\nAvailable datasets:")
for i, file in enumerate(data_files, 1):
    print(f"{i}. {os.path.basename(file)}")
choice = input("\nEnter dataset number to process or type 'all' to process all: ").strip().lower()
if choice == "all":
    selected_files = data_files
else:
    try:
        idx = int(choice) - 1
        selected_files = [data_files[idx]]
    except:
        print("Invalid input.")
        sys.exit()
for file_path in selected_files:
    dataset_name = os.path.splitext(os.path.basename(file_path))[0]
    print(f"\nProcessing dataset: {dataset_name}")        
    dataset_output = os.path.join(output_base_path, dataset_name)
    os.makedirs(dataset_output, exist_ok=True)
    metadata = load_metadata(file_path)
    with open(os.path.join(dataset_output, "metadata_summary.json"), "w") as f:
        json.dump(metadata, f, indent=4)
    cleaned_df = load_and_clean_data(file_path)
    cleaned_file = os.path.join(dataset_output, "cleaned_data.csv")
    cleaned_df.to_csv(cleaned_file, index=False)
    generate_visualizations(cleaned_df, dataset_output)
    cleaned_metadata = load_metadata(cleaned_file)
    with open(os.path.join(dataset_output, "cleaned_metadata_summary.json"), "w") as f:
        json.dump(cleaned_metadata, f, indent=4)
    global_validation_path = os.path.join(output_base_path, "validation_report.json")
    dataset_validation_path = os.path.join(dataset_output, "validation_report.json")
    if os.path.exists(global_validation_path):
        os.rename(global_validation_path, dataset_validation_path)
        print(f"Validation report saved to: {dataset_validation_path}")
print("\nAll selected datasets processed successfully!")# logic/visualize.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def generate_visualizations(df, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    # 1. Pie Chart - Count of Columns by Data Type
    dtype_counts = df.dtypes.value_counts()
    plt.figure(figsize=(6, 6))
    plt.pie(dtype_counts, labels=dtype_counts.index.astype(str), autopct='%1.1f%%', startangle=140)
    plt.title('Column Count by Data Type')
    plt.savefig(os.path.join(output_folder, "dtype_pie_chart.png"))
    plt.close()

    # 2. Bar Chart - Mean of Numeric Columns
    numeric_df = df.select_dtypes(include='number')
    if not numeric_df.empty:
        means = numeric_df.mean()
        plt.figure(figsize=(10, 5))
        means.plot(kind='bar', color='skyblue')
        plt.title("Mean of Numeric Columns")
        plt.ylabel("Mean")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(output_folder, "mean_bar_chart.png"))
        plt.close()

        # 3. Box Plot - Standard Deviation
        stds = numeric_df.std()
        plt.figure(figsize=(8, 5))
        sns.boxplot(data=stds.values)
        plt.title("Box Plot of Standard Deviations")
        plt.savefig(os.path.join(output_folder, "std_box_plot.png"))
        plt.close()

    # 4. Bar Chart - Unique Value Counts
    unique_counts = df.nunique()
    plt.figure(figsize=(10, 5))
    unique_counts.plot(kind='bar', color='orange')
    plt.title("Unique Value Count per Column")
    plt.xticks(rotation=45)
    plt.ylabel("Unique Values")
    plt.tight_layout()
    plt.savefig(os.path.join(output_folder, "unique_value_bar_chart.png"))
    plt.close()







    















