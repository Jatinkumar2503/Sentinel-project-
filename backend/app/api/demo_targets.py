from fastapi import APIRouter, Response
from fastapi.responses import HTMLResponse
from backend.app.services.chaos_lab import generate_html_v1, generate_html_v2, generate_html_v3, SAMPLE_PRODUCTS
import copy

router = APIRouter(prefix="/demo-site", tags=["Chaos Lab Demo Target"])

# Runtime state for live dynamic price drops / stockout simulations
runtime_products = copy.deepcopy(SAMPLE_PRODUCTS)

@router.get("/v1", response_class=HTMLResponse)
async def get_site_version_1():
    """Version 1.0: Baseline standard DOM hierarchy (.product-card, .price, .product-title)"""
    html = generate_html_v1(runtime_products)
    return HTMLResponse(content=html, status_code=200)

@router.get("/v2", response_class=HTMLResponse)
async def get_site_version_2():
    """Version 2.0: Mutated DOM with data-testid & renamed classes (breaks baseline scraper)"""
    html = generate_html_v2(runtime_products)
    return HTMLResponse(content=html, status_code=200)

@router.get("/v3", response_class=HTMLResponse)
async def get_site_version_3():
    """Version 3.0: Semantic Microdata hierarchy (itemprop='price', schema.org)"""
    html = generate_html_v3(runtime_products)
    return HTMLResponse(content=html, status_code=200)

@router.post("/mutate-price")
async def mutate_competitor_price(product_id: str = "LP-001", new_price: float = 129999.0):
    """Dynamically mutates a competitor price in the demo lab to trigger intelligence alert"""
    for p in runtime_products:
        if p["id"] == product_id:
            old = p["price"]
            p["price"] = new_price
            return {"status": "SUCCESS", "message": f"Updated price for {p['name']} from {old} to {new_price}"}
    return {"status": "NOT_FOUND"}

@router.post("/reset")
async def reset_demo_lab():
    """Resets demo products to baseline state"""
    global runtime_products
    runtime_products = copy.deepcopy(SAMPLE_PRODUCTS)
    return {"status": "SUCCESS", "message": "Demo lab reset to default catalog"}
