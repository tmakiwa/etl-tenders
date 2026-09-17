# Tender Data ETL Pipeline

A Python ETL project for cleaning, validating and storing tender data from CSV files.

## What It Does

The pipeline:

- Reads raw tender data from CSV
- Validates required columns
- Cleans text values
- Parses multiple date formats
- Fills missing closing dates using a defined fallback rule
- Normalises budget values
- Validates contact email addresses
- Standardises category and province values
- Removes duplicate tender records
- Calculates days remaining until closing
- Exports cleaned data to CSV
- Loads the cleaned dataset into SQLite

## Technologies

- Python
- pandas
- SQLite
- Regular Expressions
- argparse
- Git / GitHub

## Usage

```bash
python tenders_etl.py --input tenders_raw.csv --out tenders_clean.csv --db tenders.db
```

## Example Pipeline

```text
Raw CSV
   ↓
Validate required fields
   ↓
Clean and standardise values
   ↓
Parse dates and budgets
   ↓
Validate emails
   ↓
Deduplicate records
   ↓
Calculate days to close
   ↓
Clean CSV + SQLite database
```

## Purpose

This is a portfolio project demonstrating practical data cleaning, validation, transformation and database-loading workflows using Python.

## Developer

**Tinashe Makiwa**  
Web Developer – PHP, WordPress, WooCommerce and Technical SEO

Portfolio: https://tinashemakiwa.com/my-work/  
GitHub: https://github.com/tmakiwa
