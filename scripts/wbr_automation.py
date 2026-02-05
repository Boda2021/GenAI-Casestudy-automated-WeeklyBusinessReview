#!/usr/bin/env python3
"""
Complete end-to-end automation script for Weekly Business Review.
This script orchestrates the entire WBR workflow:
1. Extract data from database
2. Update Excel file
3. Generate email with charts
"""

import sys
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

from extract_data import extract_and_update_excel, DB_PATH, EXCEL_PATH, DATA_SHEET_NAME
from generate_email import refresh_pivot_table_and_chart, create_email_with_image, ANALYSIS_SHEET, VISUALIZATION_SHEET

def run_complete_automation():
    """
    Run the complete WBR automation workflow.
    """
    print("=" * 80)
    print("WEEKLY BUSINESS REVIEW AUTOMATION")
    print("=" * 80)
    print()
    
    # Step 1: Extract data and update Excel
    print("STEP 1: Extracting data from database and updating Excel...")
    print("-" * 80)
    try:
        extract_and_update_excel(
            db_path=DB_PATH,
            excel_path=EXCEL_PATH,
            sheet_name=DATA_SHEET_NAME
        )
        print("✓ Step 1 completed successfully\n")
    except Exception as e:
        print(f"✗ Step 1 failed: {e}")
        print("Please check your database connection and file paths.")
        return False
    
    # Step 2: Refresh pivot tables and extract charts
    print("STEP 2: Refreshing pivot tables and extracting charts...")
    print("-" * 80)
    try:
        chart_image_path = refresh_pivot_table_and_chart(
            excel_path=EXCEL_PATH,
            analysis_sheet=ANALYSIS_SHEET,
            visualization_sheet=VISUALIZATION_SHEET
        )
        print("✓ Step 2 completed successfully\n")
    except Exception as e:
        print(f"✗ Step 2 failed: {e}")
        print("Continuing without chart extraction...")
        chart_image_path = None
    
    # Step 3: Generate email draft
    print("STEP 3: Generating email draft...")
    print("-" * 80)
    try:
        create_email_with_image(
            image_path=chart_image_path,
            recipient='team@example.com',  # Update with actual recipient
            subject='Weekly Business Review - Automated Report'
        )
        print("✓ Step 3 completed successfully\n")
    except Exception as e:
        print(f"✗ Step 3 failed: {e}")
        print("Email generation may have failed, but data extraction completed.")
    
    print("=" * 80)
    print("AUTOMATION COMPLETE")
    print("=" * 80)
    print(f"\nExcel file updated: {EXCEL_PATH}")
    if chart_image_path:
        print(f"Chart image saved: {chart_image_path}")
    print("\nNext steps:")
    print("1. Review the Excel file for accuracy")
    print("2. Edit the email draft with your insights")
    print("3. Send the email to stakeholders")
    
    return True

if __name__ == "__main__":
    # Check if database exists
    if not DB_PATH.exists():
        print(f"Error: Database not found at {DB_PATH}")
        print("Please ensure the database file exists in the data directory.")
        exit(1)
    
    # Run automation
    success = run_complete_automation()
    
    if not success:
        exit(1)
