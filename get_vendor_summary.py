import sqlalchemy
from sqlalchemy import create_engine
import pandas as pd
import logging
from ingestion_db import ingest_db

# Setup logging
logging.basicConfig(
    filename='logs/get_vendor_summary.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='a'
)

def create_vendor_summary(engine):
    try:
        logging.info("Running SQL query to create vendor summary")
        Vendor_sales_summary = pd.read_sql_query("""
        WITH FreightSummary AS (
            SELECT VendorNumber, SUM(Freight) AS TotalFreight
            FROM vendor_invoice
            GROUP BY VendorNumber
        ),                                        
        PurchaseSummary AS (
            SELECT 
                p.VendorNumber,
                p.VendorName,
                p.Brand,
                p.Description,
                p.PurchasePrice,
                pp.Volume,
                pp.Price AS ActualPrice,
                SUM(p.Quantity) AS TotalPurchaseQuantity,
                SUM(p.Dollars) AS TotalPurchaseDollars
            FROM purchases p
            JOIN purchase_prices pp 
                ON p.Brand = pp.Brand
            WHERE p.PurchasePrice > 0
            GROUP BY 
                p.VendorNumber, p.VendorName, p.Brand, p.Description,
                p.PurchasePrice, pp.Volume, pp.Price
        ),                                        
        SalesSummary AS (
            SELECT
                VendorNo,
                Brand,
                SUM(SalesDollars) AS TotalSalesDollars,
                SUM(SalesPrice) AS TotalSalesPrice,
                SUM(SalesQuantity) AS TotalSalesQuantity,
                SUM(ExciseTax) AS TotalExciseTax
            FROM sales
            GROUP BY VendorNo, Brand
        )
        SELECT
            ps.VendorNumber,
            ps.VendorName,
            ps.Brand,
            ps.Description,
            ps.PurchasePrice,
            ps.ActualPrice,
            ps.TotalPurchaseQuantity,
            ps.Volume,
            ps.TotalPurchaseDollars,
            ss.TotalSalesDollars,
            ss.TotalSalesQuantity,
            ss.TotalSalesPrice,
            ss.TotalExciseTax,
            fs.TotalFreight
        FROM PurchaseSummary ps
        LEFT JOIN SalesSummary ss 
            ON ps.VendorNumber = ss.VendorNo
            AND ps.Brand = ss.Brand
        LEFT JOIN FreightSummary fs 
            ON ps.VendorNumber = fs.VendorNumber
        ORDER BY ps.TotalPurchaseDollars DESC
        """, engine)
        logging.info("Vendor summary created successfully")
        return Vendor_sales_summary

    except Exception as e:
        logging.error(f"Error in create_vendor_summary: {e}")
        raise


def clean_data(df):
    try:
        logging.info("Cleaning vendor summary data")
        df['Volume'] = df['Volume'].astype(float)
        df.fillna(0, inplace=True)

        df['VendorName'] = df['VendorName'].str.strip()
        df['Description'] = df['Description'].str.strip()

        # Creating new columns
        df['GrossProfit'] = df['TotalSalesDollars'] - df['TotalPurchaseDollars']
        df['ProfitMargin'] = df['GrossProfit'] / df['TotalSalesDollars'].replace(0, 1)
        df['StockTurnover'] = df['TotalSalesQuantity'] / df['TotalPurchaseQuantity'].replace(0, 1)
        df['SalesToPurchaseRatio'] = df['TotalSalesDollars'] / df['TotalPurchaseDollars'].replace(0, 1)

        logging.info("Data cleaned successfully")
        return df

    except Exception as e:
        logging.error(f"Error in clean_data: {e}")
        raise


if __name__ == "__main__":
    try:
        logging.info("Connecting to MySQL database")
        engine = create_engine("mysql+pymysql://root:root@localhost/inventory")
        logging.info("Connection successful")

        logging.info("Creating vendor summary table")
        summary_df = create_vendor_summary(engine)

        logging.info("Cleaning the vendor summary data")
        clean_df = clean_data(summary_df)

        logging.info("Ingesting cleaned vendor summary data into the database")
        ingest_db(clean_df, 'Vendor_sales_summary', engine)  # <- ingestion_db.py handles to_sql
        logging.info("Data ingestion completed successfully")

    except Exception as e:
        logging.critical(f"Pipeline failed: {e}")
        raise
