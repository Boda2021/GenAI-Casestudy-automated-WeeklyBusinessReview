# Database Schema Documentation

## Overview

The `ecommerce_data.db` SQLite database contains ecommerce business metrics for Weekly Business Review analysis.

## Tables

### daily_metrics

Stores daily aggregated business metrics.

**Columns:**
- `date_id` (INTEGER): Foreign key to dates table
- `visitors` (INTEGER): Number of unique visitors
- `purchases` (INTEGER): Number of purchases/orders
- `revenue` (DECIMAL): Total revenue for the day
- `channel_id` (INTEGER, optional): Foreign key to channels table
- `customer_type_id` (INTEGER, optional): Foreign key to customer_types table
- `category_id` (INTEGER, optional): Foreign key to product_categories table

**Sample Query:**
```sql
SELECT 
    d.date,
    SUM(dm.visitors) as total_visitors,
    SUM(dm.purchases) as total_purchases,
    SUM(dm.revenue) as total_revenue
FROM daily_metrics dm
JOIN dates d ON dm.date_id = d.date_id
GROUP BY d.date
ORDER BY d.date DESC;
```

### dates

Date dimension table for time-based analysis.

**Columns:**
- `date_id` (INTEGER): Primary key
- `date` (DATE): Actual date
- `day_of_week` (TEXT, optional): Day name (Monday, Tuesday, etc.)
- `month` (INTEGER, optional): Month number (1-12)
- `year` (INTEGER, optional): Year
- `is_weekend` (BOOLEAN, optional): Whether date is weekend

### channels

Marketing channel information.

**Columns:**
- `channel_id` (INTEGER): Primary key
- `channel_name` (TEXT): Name of marketing channel (e.g., "Email", "Social Media", "Organic Search")
- `channel_type` (TEXT, optional): Type classification

### customer_types

Customer segmentation data.

**Columns:**
- `customer_type_id` (INTEGER): Primary key
- `type_name` (TEXT): Customer type name (e.g., "New", "Returning", "VIP")
- `description` (TEXT, optional): Description of customer type

### product_categories

Product category information.

**Columns:**
- `category_id` (INTEGER): Primary key
- `category_name` (TEXT): Product category name
- `parent_category_id` (INTEGER, optional): For hierarchical categories

## Common Queries

### Weekly Summary

```sql
SELECT 
    strftime('%Y-%W', d.date) as week,
    SUM(dm.visitors) as total_visitors,
    SUM(dm.purchases) as total_purchases,
    SUM(dm.revenue) as total_revenue,
    ROUND(AVG(dm.revenue / NULLIF(dm.purchases, 0)), 2) as avg_order_value
FROM daily_metrics dm
JOIN dates d ON dm.date_id = d.date_id
GROUP BY week
ORDER BY week DESC;
```

### Channel Performance

```sql
SELECT 
    c.channel_name,
    SUM(dm.visitors) as visitors,
    SUM(dm.purchases) as purchases,
    SUM(dm.revenue) as revenue,
    ROUND(SUM(dm.revenue) / NULLIF(SUM(dm.visitors), 0), 2) as revenue_per_visitor
FROM daily_metrics dm
JOIN channels c ON dm.channel_id = c.channel_id
JOIN dates d ON dm.date_id = d.date_id
WHERE d.date >= date('now', '-30 days')
GROUP BY c.channel_name
ORDER BY revenue DESC;
```

### Customer Type Analysis

```sql
SELECT 
    ct.type_name,
    COUNT(DISTINCT dm.date_id) as days_active,
    SUM(dm.purchases) as total_purchases,
    SUM(dm.revenue) as total_revenue,
    ROUND(AVG(dm.revenue / NULLIF(dm.purchases, 0)), 2) as avg_order_value
FROM daily_metrics dm
JOIN customer_types ct ON dm.customer_type_id = ct.customer_type_id
GROUP BY ct.type_name;
```

### Category Performance

```sql
SELECT 
    pc.category_name,
    SUM(dm.purchases) as purchases,
    SUM(dm.revenue) as revenue,
    ROUND(SUM(dm.revenue) / NULLIF(SUM(dm.purchases), 0), 2) as avg_price
FROM daily_metrics dm
JOIN product_categories pc ON dm.category_id = pc.category_id
GROUP BY pc.category_name
ORDER BY revenue DESC;
```

## Data Relationships

```
dates (1) ──< (many) daily_metrics
channels (1) ──< (many) daily_metrics
customer_types (1) ──< (many) daily_metrics
product_categories (1) ──< (many) daily_metrics
```

## Notes

- All monetary values are stored as DECIMAL for precision
- Date filtering should use the `dates` table for proper time-based queries
- NULL values in foreign keys indicate metrics not broken down by that dimension
- Use `NULLIF()` to handle division by zero in calculations
