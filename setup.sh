#!/bin/bash
# Setup script for Weekly Business Review Automation

echo "Setting up Weekly Business Review Automation..."
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version || { echo "Error: Python 3 is required"; exit 1; }

# Create virtual environment (optional)
read -p "Create virtual environment? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    echo "Virtual environment activated"
fi

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Check for data files
echo ""
echo "Checking data files..."
if [ ! -f "data/ecommerce_data.db" ]; then
    echo "Warning: ecommerce_data.db not found in data/ directory"
    echo "Please copy your database file to data/ecommerce_data.db"
fi

if [ ! -f "data/WBR_Working_Sheet.xlsx" ]; then
    echo "Warning: WBR_Working_Sheet.xlsx not found in data/ directory"
    echo "Please copy your Excel template to data/WBR_Working_Sheet.xlsx"
fi

echo ""
echo "Setup complete!"
echo ""
echo "Next steps:"
echo "1. Ensure data files are in the data/ directory"
echo "2. Update email recipient in scripts/generate_email.py"
echo "3. Run: python scripts/wbr_automation.py"
