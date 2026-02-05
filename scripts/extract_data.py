#!/usr/bin/env python3
"""
Script to extract data from SQLite database and update Excel file.
This automates the data collection step of the Weekly Business Review process.
"""

import sqlite3
import pandas as pd
from pathlib import Path
import os

# Configuration - Update these paths as needed
DB_PATH = Path(__file__).parent.parent / 'data' / 'ecommerce_data.db'
EXCEL_PATH = Path(__file__).parent.parent / 'data' / 'WBR_Working_Sheet.xlsx'
DATA_SHEET_NAME = 'Data'  # Name of the sheet to update

def read_sql_query(query_file_path=None):
    """
    Read SQL query from a file or return default query.
    
    Args:
        query_file_path: Path to SQL file. If None, uses default query.
    
    Returns:
        SQL query string
    """
    if query_file_path and os.path.exists(query_file_path):
        with open(query_file_path, 'r') as file:
            return file.read()
    
    # Default query to get daily metrics
    default_query = """
    SELECT 
        d.date as Date,
        SUM(dm.visitors) as Total_Visitors,
        SUM(dm.purchases) as Total_Purchases,
        SUM(dm.revenue) as Total_Revenue,
        CASE 
            WHEN SUM(dm.purchases) > 0 
            THEN ROUND(SUM(dm.revenue) / SUM(dm.purchases), 2)
            ELSE 0 
        END as Average_Order_Value
    FROM daily_metrics dm
    JOIN dates d ON dm.date_id = d.date_id
    GROUP BY d.date
    ORDER BY d.date DESC
    LIMIT 30;
    """
    return default_query

def extract_and_update_excel(db_path, excel_path, sheet_name, sql_query=None):
    """
    Extract data from SQLite database and update Excel file.
    
    Args:
        db_path: Path to SQLite database
        excel_path: Path to Excel file
        sheet_name: Name of the sheet to update
        sql_query: SQL query string (optional)
    """
    # Read SQL query
    if sql_query is None:
        sql_query = read_sql_query()
    
    print(f"Connecting to database: {db_path}")
    
    # Connect to SQLite database
    conn = sqlite3.connect(str(db_path))
    
    try:
        # Execute the SQL query and fetch the data into a DataFrame
        print("Executing SQL query...")
        df = pd.read_sql_query(sql_query, conn)
        
        print(f"Retrieved {len(df)} rows")
        print(f"Columns: {list(df.columns)}")
        print("\nFirst few rows:")
        print(df.head())
        
        # Ensure Excel file exists or create it
        excel_path = Path(excel_path)
        if not excel_path.exists():
            print(f"Creating new Excel file: {excel_path}")
            # Create a new workbook with the data sheet
            with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name=sheet_name, index=False)
        else:
            # Update existing Excel file
            print(f"Updating Excel file: {excel_path}")
            with pd.ExcelWriter(excel_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                df.to_excel(writer, sheet_name=sheet_name, index=False)
        
        print(f"\n✓ Data successfully inserted into Excel file at sheet '{sheet_name}'")
        
    except Exception as e:
        print(f"Error: {e}")
        raise
    finally:
        # Close the database connection
        conn.close()
        print("Database connection closed")

if __name__ == "__main__":
    # Check if database exists
    if not DB_PATH.exists():
        print(f"Error: Database not found at {DB_PATH}")
        print("Please ensure the database file exists in the data directory.")
        exit(1)
    
    # Extract and update
    extract_and_update_excel(
        db_path=DB_PATH,
        excel_path=EXCEL_PATH,
        sheet_name=DATA_SHEET_NAME
    )
