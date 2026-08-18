from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.app.models.database_models import Product, ProductHistory, IntelligenceEvent, Competitor
from backend.app.core.ws_manager import ws_manager
import logging

logger = logging.getLogger(__name__)

class CompetitiveIntelligenceEngine:
    async def process_scraped_products(
        self,
        db: AsyncSession,
        competitor_id: int,
        scraped_records: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Detects price changes, stockout events, new product launches,
        and creates intelligence alerts in real-time.
        """
        generated_events = []

        # Fetch competitor info
        comp_res = await db.execute(select(Competitor).where(Competitor.id == competitor_id))
        competitor = comp_res.scalars().first()
        comp_name = competitor.name if competitor else f"Competitor #{competitor_id}"

        for record in scraped_records:
            prod_name = record.get("product_name")
            if not prod_name:
                continue

            current_price = float(record.get("price", 0.0))
            availability = record.get("availability", "in_stock")
            discount = float(record.get("discount", 0.0))
            rating = float(record.get("rating", 0.0))
            url = record.get("product_url", "#")

            # Check if product already exists
            query = select(Product).where(
                Product.competitor_id == competitor_id,
                Product.product_name == prod_name
            )
            res = await db.execute(query)
            existing_product = res.scalars().first()

            if not existing_product:
                # 1. NEW PRODUCT DETECTED
                new_prod = Product(
                    competitor_id=competitor_id,
                    sku=f"SKU-{abs(hash(prod_name)) % 100000}",
                    product_name=prod_name,
                    current_price=current_price,
                    original_price=current_price,
                    currency=record.get("currency", "INR"),
                    availability=availability,
                    discount_pct=discount,
                    rating=rating,
                    product_url=url
                )
                db.add(new_prod)
                await db.flush()

                # Add initial history
                history = ProductHistory(
                    product_id=new_prod.id,
                    price=current_price,
                    discount_pct=discount,
                    availability=availability
                )
                db.add(history)

                # Log Intelligence Event
                event = IntelligenceEvent(
                    competitor_id=competitor_id,
                    product_id=new_prod.id,
                    event_type="NEW_PRODUCT",
                    severity="INFO",
                    title=f"🆕 New Competitor Product: {prod_name[:40]}...",
                    description=f"{comp_name} launched a new item '{prod_name}' priced at ₹{current_price:,.2f}.",
                    metadata_json={
                        "product_name": prod_name,
                        "price": current_price,
                        "discount": discount,
                        "url": url
                    }
                )
                db.add(event)
                generated_events.append({"type": "NEW_PRODUCT", "title": event.title})

            else:
                old_price = existing_product.current_price
                old_avail = existing_product.availability

                # Update product snapshot
                existing_product.current_price = current_price
                existing_product.availability = availability
                existing_product.discount_pct = discount
                existing_product.rating = rating

                # Append history
                history = ProductHistory(
                    product_id=existing_product.id,
                    price=current_price,
                    discount_pct=discount,
                    availability=availability
                )
                db.add(history)

                # 2. PRICE CHANGE DETECTION
                if old_price > 0 and current_price != old_price:
                    diff_pct = ((current_price - old_price) / old_price) * 100.0
                    
                    if diff_pct < -5.0:
                        # Price Drop Alert
                        severity = "CRITICAL" if diff_pct <= -10.0 else "WARNING"
                        event = IntelligenceEvent(
                            competitor_id=competitor_id,
                            product_id=existing_product.id,
                            event_type="PRICE_DROP",
                            severity=severity,
                            title=f"📉 Price Drop ({diff_pct:.1f}%): {prod_name[:35]}...",
                            description=f"{comp_name} dropped price on '{prod_name}' from ₹{old_price:,.2f} to ₹{current_price:,.2f} ({diff_pct:.1f}% reduction).",
                            metadata_json={
                                "old_price": old_price,
                                "new_price": current_price,
                                "diff_pct": round(diff_pct, 2)
                            }
                        )
                        db.add(event)
                        generated_events.append({"type": "PRICE_DROP", "title": event.title})

                    elif diff_pct > 5.0:
                        # Price Increase
                        event = IntelligenceEvent(
                            competitor_id=competitor_id,
                            product_id=existing_product.id,
                            event_type="PRICE_INCREASE",
                            severity="INFO",
                            title=f"📈 Price Increase (+{diff_pct:.1f}%): {prod_name[:35]}...",
                            description=f"{comp_name} raised price on '{prod_name}' to ₹{current_price:,.2f} (from ₹{old_price:,.2f}).",
                            metadata_json={
                                "old_price": old_price,
                                "new_price": current_price,
                                "diff_pct": round(diff_pct, 2)
                            }
                        )
                        db.add(event)
                        generated_events.append({"type": "PRICE_INCREASE", "title": event.title})

                # 3. AVAILABILITY CHANGE DETECTION
                if old_avail != availability:
                    if availability == "out_of_stock":
                        event = IntelligenceEvent(
                            competitor_id=competitor_id,
                            product_id=existing_product.id,
                            event_type="OUT_OF_STOCK",
                            severity="WARNING",
                            title=f"⚠️ Stockout Alert: {prod_name[:35]}...",
                            description=f"{comp_name} is now OUT OF STOCK for '{prod_name}'. High opportunity window.",
                            metadata_json={"product_name": prod_name, "status": availability}
                        )
                        db.add(event)
                        generated_events.append({"type": "OUT_OF_STOCK", "title": event.title})
                    elif availability == "in_stock":
                        event = IntelligenceEvent(
                            competitor_id=competitor_id,
                            product_id=existing_product.id,
                            event_type="STOCK_REPLENISHED",
                            severity="INFO",
                            title=f"📦 Stock Replenished: {prod_name[:35]}...",
                            description=f"'{prod_name}' is back in stock at {comp_name}.",
                            metadata_json={"product_name": prod_name, "status": availability}
                        )
                        db.add(event)
                        generated_events.append({"type": "STOCK_REPLENISHED", "title": event.title})

        await db.commit()

        # Broadcast live intelligence notifications over WebSocket
        for ev in generated_events:
            await ws_manager.broadcast("INTELLIGENCE_EVENT_ALERT", ev)

        return generated_events

intelligence_engine = CompetitiveIntelligenceEngine()
