# Supplier Product Data Processing Workflow

## 1. Overview

This project demonstrates a basic supplier product-data integration workflow. Supplier records are loaded from a CSV file, standardized, transformed into consistent attributes, validated and exported for further review.

## 2. Input Data

Source file: `product_data/supplier_products.csv`

The sample dataset contains supplier product information, including:

- Supplier SKU
- Brand
- Product name
- Category
- RAM
- Storage
- Weight
- Description

## 3. Attribute Mapping

The supplier fields are mapped to standardized target attributes.

| Supplier field | Target attribute | Transformation |
|---|---|---|
| supplier_sku | supplier_sku | Retain identifier |
| brand | brand | Standardize brand names |
| product_name | product_name | Trim whitespace |
| category | category | Normalize category text |
| ram | ram_gb | Extract capacity in GB |
| storage | storage_gb | Convert capacity to GB |
| weight | weight_g | Convert kilograms to grams |
| description | description | Trim whitespace |

The detailed mapping is maintained in `product_data/attribute_mapping.xlsx`.

## 4. Processing Workflow

1. Load supplier CSV data using Pandas.
2. Check the expected input columns.
3. Standardize text fields and brand names.
4. Extract and normalize RAM, storage and weight values.
5. Validate required and optional fields.
6. Identify duplicate supplier identifiers and potential duplicate products.
7. Separate valid records from records containing errors.
8. Export the processed data and error report.

## 5. Validation and Output

The pipeline produces two output files:

- `output/cleaned_products.csv` — records that pass the pipeline's error checks, including any warnings.
- `output/error_report.csv` — records containing validation errors, with the associated error and warning information.

Missing required fields and invalid RAM or storage values are treated as errors. Missing optional fields such as weight and description are treated as warnings.

Potential duplicate products are flagged for review rather than automatically merged.

## 6. Technologies

- Python
- Pandas
- Regular expressions
- CSV
- Excel

## 7. Scope

This is a demonstration of supplier-data normalization and validation. It is not connected to a live PIM platform or supplier system.