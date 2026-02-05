#!/usr/bin/env python3
"""
Script to refresh Excel pivot tables, extract charts, and generate email draft.
This automates the data presentation step of the Weekly Business Review process.

Note: This script uses win32com for Windows. For macOS/Linux, alternative
approaches using openpyxl or other libraries may be needed.
"""

import os
import sys
from pathlib import Path

# Platform-specific imports
if sys.platform == 'win32':
    import win32com.client as win32
else:
    print("Warning: win32com is Windows-only. This script may need modifications for macOS/Linux.")
    print("Consider using openpyxl or other cross-platform libraries.")

EXCEL_PATH = Path(__file__).parent.parent / 'data' / 'WBR_Working_Sheet.xlsx'
ANALYSIS_SHEET = 'Analysis'
VISUALIZATION_SHEET = 'Visualization'
CHART_IMAGE_PATH = Path(__file__).parent.parent / 'data' / 'chart_image.png'

def refresh_pivot_table_and_chart(excel_path, analysis_sheet, visualization_sheet):
    """
    Refresh pivot table and extract chart from Excel.
    
    Args:
        excel_path: Path to Excel file
        analysis_sheet: Name of sheet with pivot table
        visualization_sheet: Name of sheet with chart
    
    Returns:
        Path to saved chart image
    """
    if sys.platform != 'win32':
        print("This function requires Windows. Skipping Excel automation.")
        return None
    
    excel_path = os.path.abspath(str(excel_path))
    image_path = os.path.abspath(str(CHART_IMAGE_PATH))
    
    print(f"Opening Excel file: {excel_path}")
    
    try:
        excel = win32.Dispatch("Excel.Application")
        excel.Visible = False
        
        # Open workbook
        wb = excel.Workbooks.Open(excel_path)
        
        # Refresh pivot table
        print(f"Refreshing pivot table in sheet '{analysis_sheet}'...")
        ws = wb.Sheets(analysis_sheet)
        try:
            pivot_table = ws.PivotTables(1)
            pivot_table.RefreshTable()
            print("✓ Pivot table refreshed")
        except Exception as e:
            print(f"Warning: Could not refresh pivot table: {e}")
        
        # Extract chart from Visualization sheet
        print(f"Extracting chart from sheet '{visualization_sheet}'...")
        chart_sheet = wb.Sheets(visualization_sheet)
        try:
            chart = chart_sheet.ChartObjects(1).Chart
            chart.Export(Filename=image_path)
            print(f"✓ Chart exported to: {image_path}")
        except Exception as e:
            print(f"Warning: Could not export chart: {e}")
            print("This may be because the chart doesn't exist or Excel automation failed.")
            image_path = None
        
        # Save and close
        wb.Save()
        wb.Close()
        excel.Quit()
        
        return image_path
        
    except Exception as e:
        print(f"Error during Excel automation: {e}")
        print("Make sure Excel is installed and the file path is correct.")
        return None

def create_email_with_image(image_path, recipient=None, subject=None):
    """
    Create email draft with chart image embedded.
    
    Args:
        image_path: Path to chart image
        recipient: Email recipient (optional)
        subject: Email subject (optional)
    """
    if sys.platform != 'win32':
        print("Email generation requires Windows Outlook.")
        print("Alternative: Generate email content as HTML/text file.")
        generate_email_content_file(image_path, recipient, subject)
        return
    
    if not image_path or not os.path.exists(image_path):
        print("Warning: Chart image not found. Creating email without image.")
        image_path = None
    
    abs_image_path = os.path.abspath(str(image_path)) if image_path else None
    
    try:
        outlook = win32.Dispatch('outlook.application')
        mail = outlook.CreateItem(0)
        
        mail.To = recipient or 'team@example.com'
        mail.Subject = subject or 'Weekly Business Review - Data Analysis Update'
        
        # Attach image and embed in body
        if abs_image_path and os.path.exists(abs_image_path):
            attachment = mail.Attachments.Add(Source=abs_image_path)
            attachment.PropertyAccessor.SetProperty(
                "http://schemas.microsoft.com/mapi/proptag/0x3712001F", 
                "ChartImage"
            )
            mail.HTMLBody = """
            <p>Hello Team,</p>
            <p>Here's the updated chart from our Weekly Business Review analysis:</p>
            <p><img src='cid:ChartImage'></p>
            <p>Key findings:</p>
            <ul>
                <li>Please review the attached Excel file for detailed metrics</li>
                <li>Highlighted cells in the Analysis tab require attention</li>
            </ul>
            <p>Best regards,<br>Analytics Team</p>
            """
        else:
            mail.HTMLBody = """
            <p>Hello Team,</p>
            <p>Please find attached the Weekly Business Review Excel file.</p>
            <p>Key findings:</p>
            <ul>
                <li>Please review the attached Excel file for detailed metrics</li>
                <li>Highlighted cells in the Analysis tab require attention</li>
            </ul>
            <p>Best regards,<br>Analytics Team</p>
            """
        
        # Display email draft (don't send automatically)
        mail.Display(True)
        print("✓ Email draft opened in Outlook")
        
    except Exception as e:
        print(f"Error creating email: {e}")
        print("Make sure Outlook is installed and configured.")
        generate_email_content_file(image_path, recipient, subject)

def generate_email_content_file(image_path, recipient=None, subject=None):
    """
    Generate email content as HTML file (cross-platform alternative).
    
    Args:
        image_path: Path to chart image
        recipient: Email recipient
        subject: Email subject
    """
    email_file = Path(__file__).parent.parent / 'data' / 'email_draft.html'
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>{subject or 'Weekly Business Review'}</title>
    </head>
    <body>
        <p>Hello Team,</p>
        <p>Here's the updated chart from our Weekly Business Review analysis:</p>
        {f'<p><img src="{image_path}" alt="WBR Chart" style="max-width: 800px;"></p>' if image_path and os.path.exists(image_path) else ''}
        <p>Key findings:</p>
        <ul>
            <li>Please review the attached Excel file for detailed metrics</li>
            <li>Highlighted cells in the Analysis tab require attention</li>
        </ul>
        <p>Best regards,<br>Analytics Team</p>
    </body>
    </html>
    """
    
    with open(email_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✓ Email content saved to: {email_file}")
    print("You can copy this content into your email client.")

if __name__ == "__main__":
    # Check if Excel file exists
    if not EXCEL_PATH.exists():
        print(f"Error: Excel file not found at {EXCEL_PATH}")
        print("Please run extract_data.py first to create/update the Excel file.")
        exit(1)
    
    # Refresh pivot table and extract chart
    chart_image_path = refresh_pivot_table_and_chart(
        excel_path=EXCEL_PATH,
        analysis_sheet=ANALYSIS_SHEET,
        visualization_sheet=VISUALIZATION_SHEET
    )
    
    # Create email draft
    create_email_with_image(
        image_path=chart_image_path,
        recipient='team@example.com',  # Update with actual recipient
        subject='Weekly Business Review - Data Analysis Update'
    )
