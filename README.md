
---

## ⚙️ Features

✅ **Automatic File Detection**  
✅ **Supports `.csv` and `.xlsx`**  
✅ **Dynamic Cleaning:**
- Fills missing numeric values with mean
- Fills datetime columns using mode
- Fills categorical columns with "Unknown"

✅ **Metadata Extraction:**
- Data type
- Null count
- Mean, median, std, min, max (if numeric)
- Skewness, kurtosis, outlier flag (optional)

✅ **Validation Report:**
- Nulls before & after cleaning
- Column-level issues
- Data consistency checks

✅ **Dynamic Visualizations (No Manual Plot Coding!):**
- Pie chart of column types
- Bar chart of numeric means
- Box plot of standard deviations
- Bar chart of unique value counts

---

## 🚀 How to Run

1. 📂 Add your messy `.csv` or `.xlsx` files to the `Datasets/` folder.

2. ▶️ Run the main script:
```bash
python main_folder/main.py
