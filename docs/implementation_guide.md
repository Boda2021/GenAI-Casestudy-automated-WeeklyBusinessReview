# Implementation Guide: Automated Weekly Business Review

## Overview

This guide provides detailed instructions for implementing the automated Weekly Business Review (WBR) system using Generative AI.

## Prerequisites

### Software Requirements

1. **Python 3.8+**
   ```bash
   python --version
   ```

2. **Required Python Packages**
   ```bash
   pip install -r requirements.txt
   ```

3. **For Windows Email Automation**
   ```bash
   pip install pywin32
   ```

4. **Microsoft Excel** (for Windows automation)
   - Required for win32com automation
   - Alternative: Use openpyxl for cross-platform Excel manipulation

5. **Microsoft Outlook** (optional, for Windows email automation)
   - Alternative: Generate HTML email files for manual sending

### Data Requirements

1. **SQLite Database**: `ecommerce_data.db`
   - Contains daily metrics, channels, customer types, etc.
   - Place in `data/` directory

2. **Excel Template**: `WBR_Working_Sheet.xlsx`
   - Should have three sheets: Data, Analysis, Visualization
   - Place in `data/` directory

## Setup Instructions

### Step 1: Clone Repository

```bash
git clone https://github.com/Boda2021/GenAI-Casestudy-automated-WeeklyBusinessReview.git
cd GenAI-Casestudy-automated-WeeklyBusinessReview
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Prepare Data Files

1. Copy your database file to `data/ecommerce_data.db`
2. Copy your Excel template to `data/WBR_Working_Sheet.xlsx`

### Step 4: Configure Scripts

Update paths in scripts if needed:
- `scripts/extract_data.py`: Update `DB_PATH` and `EXCEL_PATH` if files are in different locations
- `scripts/generate_email.py`: Update email recipient and subject

## Usage

### Option 1: Run Complete Automation

```bash
python scripts/wbr_automation.py
```

This runs all steps:
1. Extracts data from database
2. Updates Excel file
3. Refreshes pivot tables
4. Extracts charts
5. Generates email draft

### Option 2: Run Individual Steps

#### Step 1: Extract Data Only

```bash
python scripts/extract_data.py
```

This will:
- Connect to SQLite database
- Execute SQL query
- Update Excel Data sheet

#### Step 2: Generate Email Only

```bash
python scripts/generate_email.py
```

This will:
- Refresh Excel pivot tables
- Extract chart as image
- Create email draft

## Customization

### Custom SQL Queries

Create a SQL file (e.g., `data/query.sql`) and modify `extract_data.py`:

```python
sql_query = read_sql_query('data/query.sql')
```

Or pass query directly:

```python
custom_query = """
SELECT date, SUM(revenue) as total_revenue
FROM daily_metrics
GROUP BY date
"""
extract_and_update_excel(..., sql_query=custom_query)
```

### Different Database Systems

To use PostgreSQL, MySQL, or other databases:

1. Install appropriate driver:
   ```bash
   pip install psycopg2  # PostgreSQL
   pip install pymysql    # MySQL
   ```

2. Modify `extract_data.py` connection:
   ```python
   import psycopg2
   conn = psycopg2.connect(host='localhost', database='mydb', user='user', password='pass')
   ```

### Cross-Platform Email (macOS/Linux)

The email script generates HTML files as fallback. To send emails programmatically:

1. **Using SMTP**:
   ```python
   import smtplib
   from email.mime.multipart import MIMEMultipart
   from email.mime.text import MIMEText
   # ... implement SMTP sending
   ```

2. **Using Mail Libraries**:
   ```bash
   pip install yagmail  # Simple Gmail sending
   ```

## Troubleshooting

### Common Issues

#### 1. Database Connection Error

**Problem**: `sqlite3.OperationalError: unable to open database file`

**Solution**:
- Check database file path
- Ensure file permissions allow reading
- Use absolute paths if relative paths fail

#### 2. Excel File Locked

**Problem**: `PermissionError` when updating Excel

**Solution**:
- Close Excel file if open
- Check file permissions
- Ensure no other process is accessing the file

#### 3. win32com Not Available (macOS/Linux)

**Problem**: `ModuleNotFoundError: No module named 'win32com'`

**Solution**:
- This is expected on macOS/Linux
- Script will fall back to HTML email generation
- Use alternative libraries (openpyxl) for Excel manipulation

#### 4. Chart Extraction Fails

**Problem**: Chart not found or export fails

**Solution**:
- Verify Visualization sheet exists
- Check that chart is the first chart object
- Ensure Excel file has been saved with charts

#### 5. Email Not Displaying Image

**Problem**: Image doesn't appear in email

**Solution**:
- Use absolute paths for images
- Set Content-ID property correctly
- Use `cid:` reference in HTML body

## Best Practices

### 1. Error Handling

Always wrap database and file operations in try-except blocks:

```python
try:
    # Your code
except Exception as e:
    print(f"Error: {e}")
    # Handle error appropriately
```

### 2. Logging

Add logging for production use:

```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("Starting data extraction...")
```

### 3. Configuration Management

Use configuration files instead of hardcoded values:

```python
# config.yaml
database:
  path: data/ecommerce_data.db
excel:
  path: data/WBR_Working_Sheet.xlsx
  data_sheet: Data
```

### 4. Testing

Test each component separately before running full automation:

```python
# Test database connection
conn = sqlite3.connect(DB_PATH)
cursor = conn.execute("SELECT COUNT(*) FROM daily_metrics")
print(f"Rows: {cursor.fetchone()[0]}")
```

### 5. Version Control

- Don't commit sensitive data (passwords, API keys)
- Use `.gitignore` for data files if needed
- Document all dependencies

## Advanced Features

### Scheduled Automation

Use cron (Linux/macOS) or Task Scheduler (Windows):

```bash
# Run every Monday at 9 AM
0 9 * * 1 cd /path/to/repo && python scripts/wbr_automation.py
```

### Integration with Cloud Storage

Upload results to cloud storage:

```python
import boto3
s3 = boto3.client('s3')
s3.upload_file('data/WBR_Working_Sheet.xlsx', 'bucket', 'wbr/report.xlsx')
```

### API Integration

Create REST API for triggering automation:

```python
from flask import Flask
app = Flask(__name__)

@app.route('/run-wbr', methods=['POST'])
def run_wbr():
    success = run_complete_automation()
    return {'status': 'success' if success else 'failed'}
```

## Next Steps

1. Customize SQL queries for your metrics
2. Adjust Excel template for your needs
3. Set up scheduled runs
4. Integrate with your email system
5. Add data validation and quality checks
6. Implement error notifications

## Support

For issues or questions:
1. Check troubleshooting section
2. Review script comments
3. Check GitHub issues
4. Consult case study documentation
