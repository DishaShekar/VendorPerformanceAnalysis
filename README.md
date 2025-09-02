# 📊 Vendor Performance Analysis

This project analyzes vendor performance using **sales and purchase data**.  
It includes **data processing scripts**, **SQL-based summarization**, and an **interactive Power BI dashboard** for business insights.

---

## 🚀 Project Structure
Vendor_Data_Analysis/
│── get_vendor_summary.py # Python script to summarize vendor data
│── ingestion_db.py # Script to ingest and clean raw data
│── Exploratory_data_analysis.ipynb # (Optional) EDA reference notebook
│── Vendor_Performance_Analysis.ipynb # (Optional) Analysis reference notebook
│── Vendor_Performance Dashboard.pdf # Exported Power BI Dashboard
│── .gitignore # Ignore unnecessary/large files
│── README.md # Project documentation
│── data/ (not included - see dataset link below)



## 📂 Dataset

Due to GitHub's file size restrictions, the datasets are **not stored in this repository**.  
You can download them from the following link:

👉 [**Download Dataset**](https://drive.google.com/drive/folders/19AYRvg9mOh1shIGlle8uiNT1prlJcDwX?usp=sharing)

After downloading, place the files inside a `data/` folder:

Vendor_Data_Analysis/
└── data/
├── purchases.csv
├── sales.csv
├── vendor_invoice.csv
├── purchase_prices.csv


## 🔍 Key Analysis

- **Sales & Purchase Trends** – Compare vendor sales vs. purchases.  
- **Profitability Metrics** – Calculate Gross Profit & Profit Margins.  
- **Top Vendors** – Identify best-performing vendors.  
- **Low Turnover Vendors** – Detect vendors with poor stock turnover.  
- **Dashboard** – Visualize KPIs using Power BI.  

---

## 📊 Power BI Dashboard

The **Vendor Performance Dashboard** provides interactive insights:

- 📈 Total Sales, Purchases, and Gross Profit  
- 💰 Profit Margin % by Vendor  
- 🏆 Top Vendors by Sales  
- 📦 Stock Turnover & Unsold Inventory  

👉 See the dashboard here: [Vendor_Performance Dashboard.pdf](./Vendor_Performance%20Dashboard.pdf)

---

## ⚙️ How to Run (VS Code)

1. **Clone this repo:**
   ```bash
   git clone https://github.com/DishaShekar/VendorPerformanceAnalysis.git
   cd VendorPerformanceAnalysis
Install required libraries:


pip install -r requirements.txt
Download the dataset and place it in the data/ folder.

Run the scripts in VS Code:

Open the folder in VS Code

Update your MySQL connection string in get_vendor_summary.py

Run:
python get_vendor_summary.py
Explore the Dashboard in Power BI:

Open Power BI Desktop

Import the dataset or connect to your database

Use the visuals from Vendor_Performance Dashboard.pdf



## 🛠️ Tech Stack
Python → Pandas, NumPy, Matplotlib, Seaborn

SQL & SQLAlchemy → Data storage and querying

VS Code → Development environment

Power BI → Dashboard Visualization
