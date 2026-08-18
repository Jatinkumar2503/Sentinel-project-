# Bright Data Scraper Studio Integration

## Custom Scraper Studio Definition
Sentinel AI utilizes custom Scraper Studio collectors defined in `scraper_studio/custom_scraper_definition.json`.

### Extracted Target Fields
- `product_name` (String, Required)
- `product_url` (URL, Required)
- `price` (Number, Required)
- `currency` (String, ISO Code)
- `availability` (String: `in_stock`, `out_of_stock`)
- `discount` (Number: 0-100)
- `rating` (Number: 0-5.0)
- `scraped_at` (ISO DateTime)

## Collector API & CLI Usage
```bash
# Example Collector Execution via CLI
brightdata collector run --id c_sentinel_laptops_v1 --target https://example.com/products --format json
```
