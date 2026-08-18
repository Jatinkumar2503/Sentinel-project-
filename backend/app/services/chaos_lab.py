"""
Chaos Lab Target Server & HTML Generator
Generates Version 1 (Baseline), Version 2 (Selector mutation), and Version 3 (DOM hierarchy mutation)
for deterministic testing and flawless live demos.
"""
from typing import Dict, Any, List

SAMPLE_PRODUCTS = [
    {
        "id": "LP-001",
        "name": "AeroBook Pro 16 Max (Core i9, 32GB, 1TB SSD, RTX 4080)",
        "price": 149999.0,
        "currency": "INR",
        "stock": "in_stock",
        "discount": 12.5,
        "rating": 4.8,
        "url": "/products/aerobook-pro-16"
    },
    {
        "id": "LP-002",
        "name": "Zenith Ultra 14 OLED (Ryzen 9, 16GB, 512GB SSD)",
        "price": 84999.0,
        "currency": "INR",
        "stock": "in_stock",
        "discount": 8.0,
        "rating": 4.6,
        "url": "/products/zenith-ultra-14"
    },
    {
        "id": "LP-003",
        "name": "Titan Gaming Stealth 17 (Core i7, 32GB, 2TB SSD, RTX 4070)",
        "price": 124999.0,
        "currency": "INR",
        "stock": "out_of_stock",
        "discount": 15.0,
        "rating": 4.4,
        "url": "/products/titan-gaming-stealth-17"
    },
    {
        "id": "LP-004",
        "name": "Apex SlimBook Air 13 (Apple M3, 16GB, 256GB SSD)",
        "price": 99900.0,
        "currency": "INR",
        "stock": "in_stock",
        "discount": 5.0,
        "rating": 4.9,
        "url": "/products/apex-slimbook-air-13"
    },
    {
        "id": "LP-005",
        "name": "NovaCore Workstation 15 (Xeon W, 64GB, 2TB SSD, RTX A2000)",
        "price": 219000.0,
        "currency": "INR",
        "stock": "in_stock",
        "discount": 10.0,
        "rating": 4.7,
        "url": "/products/novacore-workstation-15"
    },
    {
        "id": "LP-006",
        "name": "Pulse Creator 15 (Core i7, 16GB, 1TB SSD, RTX 4060)",
        "price": 108999.0,
        "currency": "INR",
        "stock": "in_stock",
        "discount": 14.0,
        "rating": 4.5,
        "url": "/products/pulse-creator-15"
    }
]

def generate_html_v1(products: List[Dict[str, Any]] = SAMPLE_PRODUCTS) -> str:
    """Version 1: Standard CSS Classes"""
    items_html = ""
    for p in products:
        items_html += f"""
        <article class="product-card" id="item-{p['id']}">
            <h2 class="product-title">{p['name']}</h2>
            <div class="pricing-box">
                <span class="currency">{p['currency']}</span>
                <span class="price">{p['price']}</span>
                <span class="discount-tag">{p['discount']}% off</span>
            </div>
            <div class="meta-box">
                <span class="stock-status">{p['stock']}</span>
                <span class="rating-value">{p['rating']} ⭐</span>
            </div>
            <a href="{p['url']}" class="product-link">View Specs</a>
        </article>
        """
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>MegaStore Electronics - Laptops (Version 1.0)</title>
    <style>
        body {{ font-family: sans-serif; background: #0f172a; color: #f8fafc; padding: 20px; }}
        .product-card {{ background: #1e293b; border: 1px solid #334155; padding: 15px; margin-bottom: 12px; border-radius: 8px; }}
        .product-title {{ font-size: 18px; color: #38bdf8; margin: 0 0 10px 0; }}
        .price {{ font-size: 20px; font-weight: bold; color: #4ade80; }}
        .discount-tag {{ background: #ef4444; color: white; padding: 2px 6px; border-radius: 4px; font-size: 12px; }}
        .product-link {{ color: #60a5fa; text-decoration: none; display: inline-block; margin-top: 8px; }}
    </style>
</head>
<body>
    <header>
        <h1>MegaStore Laptops Catalog v1.0 [BASELINE]</h1>
        <p>Active Layout: Standard Class Names (.product-card, .price, .product-title)</p>
    </header>
    <main class="product-grid">
        {items_html}
    </main>
</body>
</html>"""

def generate_html_v2(products: List[Dict[str, Any]] = SAMPLE_PRODUCTS) -> str:
    """Version 2: Mutation to data-testid & renamed attributes (Breaks .price and .product-title)"""
    items_html = ""
    for p in products:
        items_html += f"""
        <div data-testid="product-item" data-sku="{p['id']}" class="c-item-wrapper">
            <div data-testid="product-title" class="c-item-headline">{p['name']}</div>
            <div class="c-cost-container">
                <span data-testid="currency" class="c-unit">{p['currency']}</span>
                <span data-testid="price" class="c-val-amount">{p['price']}</span>
                <span data-testid="discount" class="badge-saving">{p['discount']}% off</span>
            </div>
            <div class="c-status-row">
                <span data-testid="stock" class="pill-stock">{p['stock']}</span>
                <span data-testid="rating" class="score-stars">{p['rating']}</span>
            </div>
            <a data-testid="product-link" href="{p['url']}" class="btn-inspect">View Specs</a>
        </div>
        """
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>MegaStore Electronics - Laptops (Version 2.0 - Mutated)</title>
    <style>
        body {{ font-family: sans-serif; background: #0f172a; color: #f8fafc; padding: 20px; }}
        .c-item-wrapper {{ background: #1e293b; border: 1px solid #e11d48; padding: 15px; margin-bottom: 12px; border-radius: 8px; }}
        .c-item-headline {{ font-size: 18px; color: #fb7185; margin-bottom: 10px; }}
        .c-val-amount {{ font-size: 20px; font-weight: bold; color: #4ade80; }}
        .badge-saving {{ background: #f59e0b; color: black; padding: 2px 6px; border-radius: 4px; font-size: 12px; }}
        .btn-inspect {{ color: #38bdf8; text-decoration: none; display: inline-block; margin-top: 8px; }}
    </style>
</head>
<body>
    <header>
        <h1 style="color: #fb7185;">MegaStore Laptops Catalog v2.0 [MUTATED TESTIDS]</h1>
        <p>Simulating Modern React/Next.js migration (data-testid="price", class="c-val-amount")</p>
    </header>
    <main class="products-container">
        {items_html}
    </main>
</body>
</html>"""

def generate_html_v3(products: List[Dict[str, Any]] = SAMPLE_PRODUCTS) -> str:
    """Version 3: Deep Nested Hierarchy & Microdata/Schema.org structure"""
    items_html = ""
    for p in products:
        items_html += f"""
        <section itemscope itemtype="https://schema.org/Product" class="neo-catalog-unit">
            <header class="neo-header">
                <h3 itemprop="name" class="neo-name">{p['name']}</h3>
            </header>
            <div itemprop="offers" itemscope itemtype="https://schema.org/Offer" class="neo-offer">
                <meta itemprop="priceCurrency" content="{p['currency']}" />
                <span class="currency-symbol">{p['currency']}</span>
                <span itemprop="price" class="neo-exact-price">{p['price']}</span>
                <span class="neo-discount-value">Save {p['discount']}%</span>
                <link itemprop="availability" href="https://schema.org/{'InStock' if p['stock']=='in_stock' else 'OutOfStock'}" />
                <span class="neo-avail">Status: {p['stock']}</span>
            </div>
            <div itemprop="aggregateRating" itemscope itemtype="https://schema.org/AggregateRating" class="neo-rating">
                <span itemprop="ratingValue">{p['rating']}</span> / 5.0
            </div>
            <a itemprop="url" href="{p['url']}" class="neo-action-btn">Detailed Breakdown</a>
        </section>
        """
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>MegaStore Electronics - Laptops (Version 3.0 - Semantic Schema)</title>
    <style>
        body {{ font-family: sans-serif; background: #0f172a; color: #f8fafc; padding: 20px; }}
        .neo-catalog-unit {{ background: #1e293b; border: 1px solid #8b5cf6; padding: 15px; margin-bottom: 12px; border-radius: 8px; }}
        .neo-name {{ font-size: 18px; color: #c084fc; margin-bottom: 10px; }}
        .neo-exact-price {{ font-size: 20px; font-weight: bold; color: #34d399; }}
        .neo-action-btn {{ color: #a78bfa; text-decoration: none; display: inline-block; margin-top: 8px; }}
    </style>
</head>
<body>
    <header>
        <h1 style="color: #c084fc;">MegaStore Laptops Catalog v3.0 [SEMANTIC MICRODATA]</h1>
        <p>Simulating semantic microdata restructuring (itemprop="price", class="neo-exact-price")</p>
    </header>
    <main class="neo-grid">
        {items_html}
    </main>
</body>
</html>"""
