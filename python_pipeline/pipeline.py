
from pathlib import Path
import re
import pandas as pd

# --------------------------------------------------
# 1. PROJECT PATHS AND CONFIGURATION
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "product_data" / "supplier_products.csv"
OUTPUT_DIR = BASE_DIR / "output"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

EXPECTED_COLUMNS = [
    "supplier_sku",
    "brand",
    "product_name",
    "category",
    "ram",
    "storage",
    "weight",
    "description"
]

REQUIRED_COLUMNS = [
    "supplier_sku",
    "brand",
    "product_name",
    "category",
    "ram",
    "storage"
]

BRAND_MAPPING = {
    "lenovo": "Lenovo",
    "hp": "HP",
    "dell": "Dell",
    "asus": "ASUS"
}


# --------------------------------------------------
# 2. LOAD AND INSPECT SUPPLIER DATA
# --------------------------------------------------

def load_supplier_data(file_path):

    if not file_path.exists():
        raise FileNotFoundError(f"Input file not found: {file_path}")

    df = pd.read_csv(file_path, dtype=str)

    df.columns = df.columns.str.strip()

    print("\n--- SUPPLIER DATA INSPECTION ---")
    print(f"Total records: {len(df)}")
    print(f"Columns: {df.columns.tolist()}")
    print("\nMissing values:")
    print(df.isna().sum())

    return df


# --------------------------------------------------
# 3. VALIDATE INPUT SCHEMA
# --------------------------------------------------

def validate_schema(df):

    expected = set(EXPECTED_COLUMNS)
    actual = set(df.columns)

    missing = expected - actual
    unexpected = actual - expected

    if missing:
        raise ValueError(
            f"Missing required input columns: {sorted(missing)}"
        )

    if unexpected:
        print(f"WARNING: Unexpected columns: {sorted(unexpected)}")

    print("\nInput schema validation passed.")


# --------------------------------------------------
# 4. TEXT NORMALISATION
# --------------------------------------------------

def clean_text(value):

    if pd.isna(value):
        return None

    value = str(value).strip()

    return value if value else None


def clean_brand(value):

    value = clean_text(value)

    if value is None:
        return None

    return BRAND_MAPPING.get(value.lower(), value.title())


# --------------------------------------------------
# 5. PRODUCT ATTRIBUTE TRANSFORMATIONS
# --------------------------------------------------

def extract_ram(value):

    value = clean_text(value)

    if value is None:
        return None

    match = re.fullmatch(
        r"(\d+(?:\.\d+)?)\s*GB",
        value,
        re.IGNORECASE
    )

    return float(match.group(1)) if match else None


def extract_storage(value):

    value = clean_text(value)

    if value is None:
        return None

    match = re.fullmatch(
        r"(\d+(?:\.\d+)?)\s*(GB|TB)(?:\s+SSD)?",
        value,
        re.IGNORECASE
    )

    if not match:
        return None

    capacity = float(match.group(1))
    unit = match.group(2).upper()

    if unit == "TB":
        capacity *= 1000

    return capacity


def extract_weight(value):

    value = clean_text(value)

    if value is None:
        return None

    match = re.fullmatch(
        r"(\d+(?:\.\d+)?)\s*(KG|G)",
        value,
        re.IGNORECASE
    )

    if not match:
        return None

    weight = float(match.group(1))
    unit = match.group(2).upper()

    if unit == "KG":
        weight *= 1000

    return weight


# --------------------------------------------------
# 6. TRANSFORM SUPPLIER DATA
# --------------------------------------------------

def transform_data(df):

    cleaned = df.copy()

    cleaned["supplier_sku"] = cleaned["supplier_sku"].apply(clean_text)
    cleaned["brand"] = cleaned["brand"].apply(clean_brand)
    cleaned["product_name"] = cleaned["product_name"].apply(clean_text)
    cleaned["category"] = cleaned["category"].apply(clean_text)
    cleaned["description"] = cleaned["description"].apply(clean_text)

    cleaned["ram_gb"] = cleaned["ram"].apply(extract_ram)
    cleaned["storage_gb"] = cleaned["storage"].apply(extract_storage)
    cleaned["weight_g"] = cleaned["weight"].apply(extract_weight)

    return cleaned


# --------------------------------------------------
# 7. VALIDATE PRODUCT RECORDS
# --------------------------------------------------


def validate_records(df):

    errors = [[] for _ in range(len(df))]
    warnings = [[] for _ in range(len(df))]

    for position, (_, row) in enumerate(df.iterrows()):

        for column in REQUIRED_COLUMNS:
            if pd.isna(row[column]) or str(row[column]).strip() == "":
                errors[position].append(
                    f"Missing required field: {column}"
                )

        if pd.isna(row["ram_gb"]):
            errors[position].append("Invalid or missing RAM value")

        if pd.isna(row["storage_gb"]):
            errors[position].append("Invalid or missing storage value")

        if pd.isna(row["weight_g"]):
            warnings[position].append("Weight missing or invalid")

        if pd.isna(row["description"]):
            warnings[position].append("Description missing")

    # Identify duplicate supplier SKUs
    duplicate_mask = (
        df["supplier_sku"].notna()
        & df["supplier_sku"].duplicated(keep=False)
    )

    for position, is_duplicate in enumerate(duplicate_mask.to_numpy()):
        if is_duplicate:
            errors[position].append("Duplicate supplier SKU")

    # Identify possible product matches for manual review
    product_keys = (
        df["brand"].fillna("").str.casefold()
        + "|"
        + df["product_name"].fillna("").str.casefold()
    )

    possible_duplicates = (
        product_keys.ne("|")
        & product_keys.duplicated(keep=False)
    )

    for position, is_duplicate in enumerate(
        possible_duplicates.to_numpy()
    ):
        if is_duplicate:
            warnings[position].append(
                "Possible matching product: review before merging"
            )

    df["errors"] = ["; ".join(items) for items in errors]
    df["warnings"] = ["; ".join(items) for items in warnings]

    return df


# --------------------------------------------------
# 8. SEPARATE VALID AND INVALID RECORDS
# --------------------------------------------------

def prepare_output(df):

    valid_records = df[df["errors"] == ""].copy()
    invalid_records = df[df["errors"] != ""].copy()

    clean_columns = [
        "supplier_sku",
        "brand",
        "product_name",
        "category",
        "ram_gb",
        "storage_gb",
        "weight_g",
        "description",
        "warnings"
    ]

    return (
        valid_records[clean_columns],
        invalid_records
    )


# --------------------------------------------------
# 9. EXPORT RESULTS
# --------------------------------------------------

def export_results(cleaned, errors):

    cleaned_file = OUTPUT_DIR / "cleaned_products.csv"
    error_file = OUTPUT_DIR / "error_report.csv"

    cleaned.to_csv(cleaned_file, index=False)
    errors.to_csv(error_file, index=False)

    print("\n--- EXPORT SUMMARY ---")
    print(f"Clean records: {len(cleaned)}")
    print(f"Records requiring correction: {len(errors)}")
    print(f"Cleaned file: {cleaned_file}")
    print(f"Error report: {error_file}")


# --------------------------------------------------
# 10. MAIN PIPELINE
# --------------------------------------------------

def main():

    df = load_supplier_data(INPUT_FILE)

    validate_schema(df)

    transformed = transform_data(df)

    validated = validate_records(transformed)

    cleaned, errors = prepare_output(validated)

    export_results(cleaned, errors)

    print("\nPipeline execution completed.")


if __name__ == "__main__":
    main()
