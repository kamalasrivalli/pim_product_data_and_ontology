
import pandas as pd
import pytest

from python_pipeline import pipeline


@pytest.fixture
def sample_data():
    return pd.DataFrame([
        {
            "supplier_sku": "LNV101",
            "brand": "LENOVO",
            "product_name": "ThinkPad E14",
            "category": "Laptops",
            "ram": "16GB",
            "storage": "512GB SSD",
            "weight": "1.5kg",
            "description": "Business laptop",
        },
        {
            "supplier_sku": "HP202",
            "brand": "HP",
            "product_name": "ProBook 450",
            "category": "Laptops",
            "ram": "8GB",
            "storage": "256GB SSD",
            "weight": None,
            "description": None,
        },
    ])


def test_clean_brand():
    assert pipeline.clean_brand("LENOVO") == "Lenovo"
    assert pipeline.clean_brand("hp") == "HP"


def test_extract_ram():
    assert pipeline.extract_ram("16GB") == 16
    assert pipeline.extract_ram("8 GB") == 8
    assert pipeline.extract_ram("invalid") is None


def test_extract_storage():
    assert pipeline.extract_storage("512 GB SSD") == 512
    assert pipeline.extract_storage("1TB SSD") == 1000
    assert pipeline.extract_storage("invalid") is None


def test_extract_weight():
    assert pipeline.extract_weight("1.5kg") == 1500
    assert pipeline.extract_weight("1500 g") == 1500
    assert pipeline.extract_weight("invalid") is None


def test_transform_data(sample_data):
    result = pipeline.transform_data(sample_data)

    assert result.loc[0, "brand"] == "Lenovo"
    assert result.loc[0, "ram_gb"] == 16
    assert result.loc[0, "storage_gb"] == 512
    assert result.loc[0, "weight_g"] == 1500


def test_validate_schema_passes(sample_data):
    pipeline.validate_schema(sample_data)


def test_validate_schema_detects_missing_column(sample_data):
    incomplete = sample_data.drop(columns=["brand"])

    with pytest.raises(ValueError, match="Missing required input columns"):
        pipeline.validate_schema(incomplete)


def test_missing_optional_fields_are_warnings(sample_data):
    transformed = pipeline.transform_data(sample_data)
    result = pipeline.validate_records(transformed)

    second_record = result.iloc[1]

    assert "Weight missing or invalid" in second_record["warnings"]
    assert "Description missing" in second_record["warnings"]
    assert second_record["errors"] == ""


def test_missing_required_field_is_error(sample_data):
    sample_data.loc[0, "supplier_sku"] = None

    transformed = pipeline.transform_data(sample_data)
    result = pipeline.validate_records(transformed)

    assert "Missing required field: supplier_sku" in result.loc[0, "errors"]


def test_duplicate_supplier_skus_are_detected(sample_data):
    sample_data.loc[1, "supplier_sku"] = "LNV101"

    transformed = pipeline.transform_data(sample_data)
    result = pipeline.validate_records(transformed)

    assert "Duplicate supplier SKU" in result.loc[0, "errors"]
    assert "Duplicate supplier SKU" in result.loc[1, "errors"]


def test_possible_duplicate_products_are_warnings(sample_data):
    sample_data.loc[1, "brand"] = "lenovo"
    sample_data.loc[1, "product_name"] = "ThinkPad E14"

    transformed = pipeline.transform_data(sample_data)
    result = pipeline.validate_records(transformed)

    assert "Possible matching product" in result.loc[0, "warnings"]
    assert "Possible matching product" in result.loc[1, "warnings"]


def test_validate_records_handles_nonconsecutive_index(sample_data):
    sample_data.index = [10, 20]

    transformed = pipeline.transform_data(sample_data)
    result = pipeline.validate_records(transformed)

    assert len(result) == 2
    assert result.loc[10, "errors"] == ""
    assert result.loc[20, "errors"] == ""


def test_prepare_output_separates_valid_and_invalid(sample_data):
    sample_data.loc[1, "supplier_sku"] = None

    transformed = pipeline.transform_data(sample_data)
    validated = pipeline.validate_records(transformed)

    cleaned, errors = pipeline.prepare_output(validated)

    assert len(cleaned) == 1
    assert len(errors) == 1
    assert cleaned.iloc[0]["supplier_sku"] == "LNV101"


def test_load_supplier_data_missing_file(tmp_path):
    missing_file = tmp_path / "missing.csv"

    with pytest.raises(FileNotFoundError):
        pipeline.load_supplier_data(missing_file)


def test_export_results(tmp_path, monkeypatch, sample_data):
    monkeypatch.setattr(pipeline, "OUTPUT_DIR", tmp_path)

    transformed = pipeline.transform_data(sample_data)
    validated = pipeline.validate_records(transformed)
    cleaned, errors = pipeline.prepare_output(validated)

    pipeline.export_results(cleaned, errors)

    assert (tmp_path / "cleaned_products.csv").exists()
    assert (tmp_path / "error_report.csv").exists()

    exported = pd.read_csv(tmp_path / "cleaned_products.csv")
    assert len(exported) == 2
