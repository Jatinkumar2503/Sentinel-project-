from typing import Dict, Any, List, Tuple
from pydantic import ValidationError
from backend.app.schemas.product_schema import BrightDataScrapedProduct
import logging

logger = logging.getLogger(__name__)

class ValidationEngine:
    def __init__(self):
        self.pass_threshold = 90.0

    def validate_dataset(
        self,
        records: List[Dict[str, Any]],
        expected_records_count: int = 6
    ) -> Dict[str, Any]:
        """
        Runs four rigorous validation layers on scraped candidate records.
        """
        if not records:
            return {
                "verdict": "REJECTED",
                "validation_score": 0.0,
                "structural_pass_pct": 0.0,
                "statistical_pass_pct": 0.0,
                "business_pass_pct": 0.0,
                "valid_records": [],
                "quarantined_records": [],
                "failure_reasons": ["Empty dataset provided for validation."]
            }

        valid_records = []
        quarantined_records = []
        failure_reasons = []

        # Layer 1: Structural Pydantic Validation
        struct_valid = 0
        for r in records:
            try:
                validated_model = BrightDataScrapedProduct(**r)
                valid_records.append(validated_model.model_dump())
                struct_valid += 1
            except ValidationError as ve:
                quarantined_records.append({"record": r, "error": str(ve)})
                failure_reasons.append(f"Structural validation failed for product '{r.get('product_name', 'Unknown')}': {ve.errors()[0]['msg']}")

        struct_pass_pct = (struct_valid / len(records)) * 100.0

        # Layer 2: Business Rule Invariants
        biz_valid = 0
        for r in valid_records:
            price = r.get("price")
            discount = r.get("discount", 0.0)
            rating = r.get("rating", 0.0)

            passes_biz = True
            if price is None or price <= 0:
                passes_biz = False
                failure_reasons.append(f"Business invariant violation: invalid price {price}")
            if discount < 0.0 or discount > 100.0:
                passes_biz = False
                failure_reasons.append(f"Business invariant violation: discount out of range {discount}%")
            if rating < 0.0 or rating > 5.0:
                passes_biz = False
                failure_reasons.append(f"Business invariant violation: rating out of bounds {rating}")

            if passes_biz:
                biz_valid += 1

        biz_pass_pct = (biz_valid / max(len(valid_records), 1)) * 100.0 if valid_records else 0.0

        # Layer 3: Statistical Sanity / Distribution
        stat_pass_pct = 100.0
        prices = [r["price"] for r in valid_records if "price" in r and r["price"] is not None]
        if prices and len(prices) >= 3:
            avg_price = sum(prices) / len(prices)
            # Check for insane zero or billion outliers
            outliers = [p for p in prices if p > avg_price * 10 or p < avg_price * 0.05]
            if outliers:
                stat_pass_pct = max(0.0, 100.0 - (len(outliers) / len(prices)) * 100.0)
                failure_reasons.append(f"Statistical outlier detected in prices: {outliers}")

        # Layer 4: Volumetric Completeness check
        volumetric_pct = min(100.0, (len(valid_records) / max(expected_records_count, 1)) * 100.0)

        # Composite Validation Score
        composite_validation_score = round(
            (0.40 * struct_pass_pct) +
            (0.30 * biz_pass_pct) +
            (0.15 * stat_pass_pct) +
            (0.15 * volumetric_pct),
            2
        )

        if composite_validation_score >= self.pass_threshold:
            verdict = "PASSED"
        elif composite_validation_score >= 50.0:
            verdict = "QUARANTINED"
        else:
            verdict = "REJECTED"

        return {
            "verdict": verdict,
            "validation_score": composite_validation_score,
            "structural_pass_pct": round(struct_pass_pct, 2),
            "business_pass_pct": round(biz_pass_pct, 2),
            "statistical_pass_pct": round(stat_pass_pct, 2),
            "volumetric_pass_pct": round(volumetric_pct, 2),
            "valid_records": valid_records,
            "quarantined_records": quarantined_records,
            "failure_reasons": failure_reasons
        }

validation_engine = ValidationEngine()
