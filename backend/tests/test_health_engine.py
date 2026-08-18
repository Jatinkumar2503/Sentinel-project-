import pytest
from backend.app.services.health_monitor import health_monitor

def test_healthy_run_evaluation():
    perfect_records = [
        {
            "product_name": "AeroBook Pro 16",
            "product_url": "https://example.com/p/1",
            "price": 149999.0,
            "currency": "INR",
            "availability": "in_stock",
            "discount": 10.0,
            "rating": 4.8,
            "scraped_at": "2026-08-19T20:00:00"
        }
        for _ in range(6)
    ]
    report = health_monitor.evaluate_run(perfect_records, expected_count=6)
    assert report["composite_health_score"] >= 95.0
    assert report["is_degraded"] is False
    assert report["completeness"] == 100.0

def test_missing_price_degradation():
    degraded_records = [
        {
            "product_name": f"Laptop {i}",
            "product_url": f"https://example.com/p/{i}",
            "price": None,  # Broken price selector
            "currency": "INR",
            "availability": "in_stock",
            "discount": 0.0,
            "rating": 4.0,
            "scraped_at": "2026-08-19T20:00:00"
        }
        for i in range(6)
    ]
    report = health_monitor.evaluate_run(degraded_records, expected_count=6)
    assert report["composite_health_score"] < 70.0
    assert report["is_degraded"] is True
    assert any("price" in issue for issue in report["issues_detected"])

def test_empty_dataset_critical_failure():
    report = health_monitor.evaluate_run([], expected_count=6)
    assert report["composite_health_score"] == 0.0
    assert report["is_degraded"] is True
