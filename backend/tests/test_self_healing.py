import pytest
from bs4 import BeautifulSoup
from backend.app.services.self_healer import self_healer
from backend.app.services.chaos_lab import generate_html_v1, generate_html_v2, generate_html_v3
from backend.app.services.bright_data_service import DEFAULT_SELECTORS

@pytest.mark.asyncio
async def test_self_healing_recovers_v2_mutation():
    html_v2 = generate_html_v2()
    soup = BeautifulSoup(html_v2, "html.parser")
    
    # Old selectors (targeted for v1) will fail on v2
    repaired_selectors, dom_diff = self_healer._repair_selectors(soup, DEFAULT_SELECTORS)
    
    # Check that price selector was repaired to data-testid or c-val-amount
    assert "[data-testid='price']" in repaired_selectors["price"] or ".c-val-amount" in repaired_selectors["price"]
    assert "[data-testid='product-title']" in repaired_selectors["product_name"] or ".c-item-headline" in repaired_selectors["product_name"]
    
    # Now run full heal_scraper workflow against HTML v2
    result = await self_healer.heal_scraper(
        scraper_id=1,
        target_url="http://test-server/v2",
        current_selectors=DEFAULT_SELECTORS,
        broken_records_count=0,
        health_before=28.5,
        html_override=html_v2
    )
    
    assert result["status"] == "RESTORED"
    assert result["health_after"] >= 90.0
    assert result["records_after"] == 6

@pytest.mark.asyncio
async def test_self_healing_recovers_v3_semantic_microdata():
    html_v3 = generate_html_v3()
    soup = BeautifulSoup(html_v3, "html.parser")
    
    repaired_selectors, dom_diff = self_healer._repair_selectors(soup, DEFAULT_SELECTORS)
    assert "[itemprop='price']" in repaired_selectors["price"] or ".neo-exact-price" in repaired_selectors["price"]
    assert "[itemprop='name']" in repaired_selectors["product_name"] or ".neo-name" in repaired_selectors["product_name"]
