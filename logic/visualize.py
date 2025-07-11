# logic/visualize.py
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












