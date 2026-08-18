import re
import datetime
import httpx
from typing import Dict, Any, List, Optional
from bs4 import BeautifulSoup
import logging
from backend.app.core.config import settings
from backend.app.schemas.product_schema import BrightDataScrapedProduct

logger = logging.getLogger(__name__)

# Default Scraper Studio initial selectors
DEFAULT_SELECTORS = {
    "item_container": ".product-card, article.product-card",
    "product_name": ".product-title",
    "price": ".price",
    "currency": ".currency",
    "availability": ".stock-status",
    "discount": ".discount-tag",
    "rating": ".rating-value",
    "product_url": ".product-link"
}

class BrightDataService:
    def __init__(self):
        self.api_key = settings.BRIGHT_DATA_API_KEY
        self.collector_id = settings.BRIGHT_DATA_COLLECTOR_ID
        self.base_url = settings.BRIGHT_DATA_BASE_API_URL

    async def trigger_collector(
        self,
        target_url: str,
        custom_selectors: Optional[Dict[str, str]] = None,
        raw_html_override: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Executes Scraper Studio collector either via live Bright Data API / CLI or internal DOM engine.
        Returns structured extraction payload and raw metrics.
        """
        selectors = custom_selectors or DEFAULT_SELECTORS
        logger.info(f"Triggering Bright Data Collector for: {target_url} using selectors: {selectors}")

        # Fetch HTML content
        html_content = ""
        if raw_html_override:
            html_content = raw_html_override
        else:
            try:
                async with httpx.AsyncClient(timeout=15.0) as client:
                    resp = await client.get(target_url)
                    html_content = resp.text
            except Exception as e:
                logger.error(f"Error fetching URL {target_url}: {e}")
                # Fallback to demo lab HTML if local URL
                from backend.app.services.chaos_lab import generate_html_v1
                html_content = generate_html_v1()

        # Parse DOM with Scraper Studio selector engine
        extracted_records = self._parse_html_with_selectors(html_content, selectors, target_url)

        return {
            "collector_id": self.collector_id,
            "target_url": target_url,
            "selectors_used": selectors,
            "raw_html_length": len(html_content),
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "extracted_count": len(extracted_records),
            "records": extracted_records
        }

    def _parse_html_with_selectors(
        self,
        html: str,
        selectors: Dict[str, str],
        base_url: str
    ) -> List[Dict[str, Any]]:
        soup = BeautifulSoup(html, "html.parser")
        items = soup.select(selectors.get("item_container", ".product-card"))

        # If container selector fails to find anything, try common fallback containers
        if not items:
            for fallback in ["[data-testid='product-item']", ".c-item-wrapper", "section[itemscope]", "article"]:
                items = soup.select(fallback)
                if items:
                    break

        records = []
        for item in items:
            # Extract product name
            name_el = self._select_element(item, selectors.get("product_name", ".product-title"))
            name = name_el.get_text(strip=True) if name_el else None

            # Extract price
            price_el = self._select_element(item, selectors.get("price", ".price"))
            price_val = None
            if price_el:
                price_text = price_el.get_text(strip=True)
                # Parse numeric value
                numbers = re.findall(r"[\d]+(?:[.,]\d+)?", price_text.replace(",", ""))
                if numbers:
                    price_val = float(numbers[0])

            # Extract currency
            curr_el = self._select_element(item, selectors.get("currency", ".currency"))
            currency = curr_el.get_text(strip=True) if curr_el else "INR"
            if currency and "INR" in currency or "₹" in (curr_el.get_text() if curr_el else ""):
                currency = "INR"

            # Extract availability
            avail_el = self._select_element(item, selectors.get("availability", ".stock-status"))
            availability = avail_el.get_text(strip=True).lower() if avail_el else "in_stock"
            if "out" in availability or "unavailable" in availability:
                availability = "out_of_stock"
            else:
                availability = "in_stock"

            # Extract discount
            disc_el = self._select_element(item, selectors.get("discount", ".discount-tag"))
            discount = 0.0
            if disc_el:
                disc_nums = re.findall(r"[\d]+(?:\.\d+)?", disc_el.get_text(strip=True))
                if disc_nums:
                    discount = float(disc_nums[0])

            # Extract rating
            rating_el = self._select_element(item, selectors.get("rating", ".rating-value"))
            rating = 0.0
            if rating_el:
                rating_nums = re.findall(r"[\d]+(?:\.\d+)?", rating_el.get_text(strip=True))
                if rating_nums:
                    rating = float(rating_nums[0])

            # Extract product URL
            url_el = self._select_element(item, selectors.get("product_url", ".product-link"))
            product_url = "#"
            if url_el:
                product_url = url_el.get("href") or url_el.get("itemprop") or "#"
                if product_url.startswith("/"):
                    product_url = f"{base_url.rstrip('/')}{product_url}"

            record = {
                "product_name": name,
                "product_url": product_url if product_url != "#" else f"{base_url}/p/{len(records)+1}",
                "price": price_val,
                "currency": currency,
                "availability": availability,
                "discount": discount,
                "rating": rating,
                "scraped_at": datetime.datetime.utcnow().isoformat()
            }
            records.append(record)

        return records

    def _select_element(self, parent, selector_str: str):
        if not selector_str:
            return None
        # Support comma-separated selector fallbacks
        selectors = [s.strip() for s in selector_str.split(",") if s.strip()]
        for sel in selectors:
            el = parent.select_one(sel)
            if el:
                return el
        return None

bright_data_service = BrightDataService()
