# Quick Start Guide

Get up and running with the Weekly Business Review automation in 5 minutes!

## Prerequisites

- Python 3.8 or higher
- SQLite database file (`ecommerce_data.db`)
- Excel template file (`WBR_Working_Sheet.xlsx`)

## Installation

### Option 1: Using Setup Script (Recommended)

**macOS/Linux:**
```bash
chmod +x setup.sh
./setup.sh
```

**Windows:**
```cmd
setup.bat
```

### Option 2: Manual Installation

```bash
# Install dependencies
pip install -r requirements.txt

# For Windows email automation
pip install pywin32
```

## Quick Test

1. **Verify data files are present:**
   ```bash
   ls data/
   # Should show: ecommerce_data.db and WBR_Working_Sheet.xlsx
   ```

2. **Run data extraction:**
   ```bash
   python scripts/extract_data.py
   ```

3. **Check Excel file was updated:**
   - Open `data/WBR_Working_Sheet.xlsx`
   - Verify the "Data" sheet has been populated

## Running the Complete Automation

```bash
python scripts/wbr_automation.py
```

This will:
1. ✅ Extract data from database
2. ✅ Update Excel file
3. ✅ Refresh pivot tables (Windows only)
4. ✅ Extract charts (Windows only)
5. ✅ Generate email draft

## Next Steps

1. **Customize email recipient:**
   - Edit `scripts/generate_email.py`
   - Update `recipient` parameter in `create_email_with_image()`

2. **Modify SQL query:**
   - Edit `scripts/extract_data.py`
   - Update the `read_sql_query()` function or pass custom query

3. **Schedule automation:**
   - Set up cron job (Linux/macOS) or Task Scheduler (Windows)
   - Run weekly: `python scripts/wbr_automation.py`

## Troubleshooting

### Database not found
- Ensure `ecommerce_data.db` is in `data/` directory
- Check file permissions

### Excel file locked
- Close Excel if it's open
- Check file permissions

### Email not working (macOS/Linux)
- This is expected - script will generate HTML email file instead
- Check `data/email_draft.html`

## Need Help?

- See [Implementation Guide](docs/implementation_guide.md) for detailed instructions
- Check [Data Schema](docs/data_schema.md) for database structure
- Review [README.md](README.md) for full documentation
