import pytest
from backend.app.services.validation_engine import validation_engine

def test_validation_passes_valid_data():
    valid_data = [
        {
            "product_name": "Zenith Ultra 14",
            "product_url": "https://example.com/p/2",
            "price": 84999.0,
            "currency": "INR",
            "availability": "in_stock",
            "discount": 8.0,
            "rating": 4.6,
            "scraped_at": "2026-08-19T20:00:00"
        }
        for _ in range(6)
    ]
    res = validation_engine.validate_dataset(valid_data, expected_records_count=6)
    assert res["verdict"] == "PASSED"
    assert res["validation_score"] >= 90.0
    assert len(res["valid_records"]) == 6

def test_validation_rejects_negative_price():
    invalid_data = [
        {
            "product_name": "Broken Laptop",
            "product_url": "https://example.com/p/3",
            "price": -500.0,  # Negative price invariant breach
            "currency": "INR",
            "availability": "in_stock",
            "discount": 10.0,
            "rating": 4.0,
            "scraped_at": "2026-08-19T20:00:00"
        }
    ]
    res = validation_engine.validate_dataset(invalid_data, expected_records_count=1)
    assert res["verdict"] == "REJECTED"
    assert len(res["quarantined_records"]) == 1

def test_validation_quarantines_extreme_discount():
    invalid_discount = [
        {
            "product_name": "Crazy Discount Laptop",
            "product_url": "https://example.com/p/4",
            "price": 50000.0,
            "currency": "INR",
            "availability": "in_stock",
            "discount": 150.0,  # Discount > 100%
            "rating": 4.5,
            "scraped_at": "2026-08-19T20:00:00"
        }
    ]
    res = validation_engine.validate_dataset(invalid_discount, expected_records_count=1)
    assert res["verdict"] in ["REJECTED", "QUARANTINED"]
