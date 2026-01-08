# Cleans JSON strings and extracts prices
import json
from datetime import datetime, timezone
from typing import Optional, List, Any
from .models import MarketRecord

def safe_json_load(value: Any) -> Any:
    # Helper method to safely parse a value if it is a JSON string, otherwise just return it.
    if isinstance(value, str):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return None
    return value

def calculate_hours_left(end_date_str: str) -> float:
    # Calculates remaining hours from now to end date
    if not end_date_str:
        return -1.0
    
    try:
        # Polymarket dates are in ISO 8601
        end_dt = datetime.fromisoformat(end_date_str.replace('Z', '+00:00'))
        now = datetime.now(timezone.utc)
        diff = end_dt - now
        return round(diff.total_seconds() / 3600, 2)
    except Exception:
        return -1.0

def parse_market(raw: dict) -> MarketRecord:
    # convert raw api dict into market record structure
    record = MarketRecord(
        id=raw.get("id", ""),
        question=raw.get("question", "Unknown Question"),
        category=raw.get("category", "Uncategorized"),
        slug=raw.get("slug"),
        active=raw.get("active", False),
        closed=raw.get("closed", False),
        enable_order_book=raw.get("enableOrderBook", False),
        end_date_iso=raw.get("endDate")
    )

    # calc remaining time
    record.hours_to_close = calculate_hours_left(record.end_date_iso)

    # parse json fields
    outcomes = safe_json_load(raw.get("outcomes"))
    prices = safe_json_load(raw.get("outcomePrices"))
    token_ids = safe_json_load(raw.get("clobTokenIds"))

    # Validate if its a binary market
    if not isinstance(outcomes, list) or len(outcomes) != 2:
        record.invalid_reason = "Not a binary market (must have 2 outcomes)"
        return record

    # Map Tokens ["Yes", "No"]
    if isinstance(token_ids, list) and len(token_ids) == 2:
        record.yes_token_id = token_ids[0]
        record.no_token_id = token_ids[1]
    else:
        record.invalid_reason = "Missing or invalid token IDs"

    # Map Prices
    if isinstance(prices, list) and len(prices) == 2:
        try:
            record.yes_price = float(prices[0])
            record.no_price = float(prices[1])
        except (ValueError, TypeError):
             record.invalid_reason = "Price data is malformed"
    else:
        # no price data
        pass

    return record