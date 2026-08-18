from typing import Dict, Any, List, Optional
from pydantic import ValidationError
from backend.app.schemas.product_schema import BrightDataScrapedProduct
import logging

logger = logging.getLogger(__name__)

class ScraperHealthMonitor:
    def __init__(self):
        self.critical_threshold = 70.0

    def evaluate_run(
        self,
        records: List[Dict[str, Any]],
        expected_count: Optional[int] = None,
        historical_records: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Evaluates extraction health across 5 critical dimensions.
        Returns composite health score (0 - 100%) and sub-scores.
        """
        issues_detected = []
        total_records = len(records)

        if total_records == 0:
            return {
                "completeness": 0.0,
                "schema_validity": 0.0,
                "volumetric_consistency": 0.0,
                "historical_consistency": 0.0,
                "anomaly_score": 0.0,
                "composite_health_score": 0.0,
                "is_degraded": True,
                "issues_detected": ["Zero records extracted. Complete selector failure."]
            }

        # 1. Completeness Score (Weight: 30%)
        # Check non-null presence of mandatory fields: product_name, price, availability, product_url
        mandatory_fields = ["product_name", "price", "availability", "product_url"]
        total_mandatory_slots = total_records * len(mandatory_fields)
        filled_slots = 0
        missing_counts = {k: 0 for k in mandatory_fields}

        for r in records:
            for field in mandatory_fields:
                val = r.get(field)
                if val is not None and val != "" and val != "#":
                    filled_slots += 1
                else:
                    missing_counts[field] += 1

        completeness_pct = (filled_slots / total_mandatory_slots) * 100.0
        for field, count in missing_counts.items():
            if count > 0:
                missing_pct = (count / total_records) * 100.0
                issues_detected.append(f"Field '{field}' missing in {missing_pct:.1f}% of records ({count}/{total_records}).")

        # 2. Schema Validity Score (Weight: 20%)
        # Validate against strict Pydantic model
        valid_schema_records = 0
        for r in records:
            try:
                BrightDataScrapedProduct(**r)
                valid_schema_records += 1
            except ValidationError as ve:
                pass
            except Exception:
                pass

        schema_validity_pct = (valid_schema_records / total_records) * 100.0
        if schema_validity_pct < 90.0:
            issues_detected.append(f"Schema validity failure: only {schema_validity_pct:.1f}% passed Pydantic type checks.")

        # 3. Volumetric Consistency Score (Weight: 20%)
        # Compares actual record count with expected benchmark (default 6 items for demo lab)
        target_expected = expected_count if expected_count and expected_count > 0 else (len(historical_records) if historical_records else total_records)
        if target_expected > 0:
            count_ratio = min(total_records / target_expected, target_expected / total_records)
            volumetric_pct = count_ratio * 100.0
        else:
            volumetric_pct = 100.0

        if volumetric_pct < 70.0:
            issues_detected.append(f"Volumetric variance: extracted {total_records} vs expected {target_expected}.")

        # 4. Historical Consistency Score (Weight: 15%)
        # Checks if key product identifiers match previous historical runs
        if historical_records and len(historical_records) > 0:
            hist_names = set(h.get("product_name") for h in historical_records if h.get("product_name"))
            curr_names = set(r.get("product_name") for r in records if r.get("product_name"))
            overlap = hist_names.intersection(curr_names)
            historical_pct = (len(overlap) / max(len(hist_names), 1)) * 100.0
        else:
            historical_pct = 100.0

        # 5. Anomaly Score (Weight: 15%)
        # Check price presence and numeric distribution anomalies
        valid_prices = [r["price"] for r in records if r.get("price") is not None and isinstance(r.get("price"), (int, float))]
        if len(records) > 0:
            if len(valid_prices) == 0:
                # Critical anomaly: Expected prices but found none
                anomaly_pct = 0.0
                issues_detected.append("Zero valid prices extracted from records.")
            else:
                price_anomaly_count = 0
                for p in valid_prices:
                    if p <= 0 or p > 10000000:  # anomalous negative or > 1 Crore
                        price_anomaly_count += 1
                anomaly_pct = max(0.0, 100.0 - (price_anomaly_count / total_records) * 100.0)
                if price_anomaly_count > 0:
                    issues_detected.append(f"{price_anomaly_count} records have anomalous price values (<= 0 or extreme).")
        else:
            anomaly_pct = 0.0

        # Composite Health Score Calculation
        composite_score = (
            0.30 * completeness_pct +
            0.20 * schema_validity_pct +
            0.20 * volumetric_pct +
            0.15 * historical_pct +
            0.15 * anomaly_pct
        )
        
        # If any mandatory field has 0% presence across all records, cap maximum health score at 55.0
        if any(missing_counts[f] == total_records for f in mandatory_fields):
            composite_score = min(composite_score, 55.0)

        composite_score = round(max(0.0, min(100.0, composite_score)), 2)

        is_degraded = composite_score < self.critical_threshold

        return {
            "completeness": round(completeness_pct, 2),
            "schema_validity": round(schema_validity_pct, 2),
            "volumetric_consistency": round(volumetric_pct, 2),
            "historical_consistency": round(historical_pct, 2),
            "anomaly_score": round(anomaly_pct, 2),
            "composite_health_score": composite_score,
            "is_degraded": is_degraded,
            "issues_detected": issues_detected
        }

health_monitor = ScraperHealthMonitor()
