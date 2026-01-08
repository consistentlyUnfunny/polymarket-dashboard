# Logic for the 48h and status filters

from typing import List
from .models import MarketRecord

def filter_candidates(markets: List[MarketRecord]) -> List[MarketRecord]:
    '''
    Filters the raw market list down to valid candidates.
    these condition need to be fulfilled: Active, Order Book Enabled, Closing in 0-48 hours.
    '''
    candidates = []

    for m in markets:
        # skip if data invalid during processing
        if m.invalid_reason:
            continue

        # status check
        if not (m.active and not m.closed and m.enable_order_book):
            continue

        # time check
        if m.hours_to_close is None:
            continue
            
        if not (0 < m.hours_to_close <= 48):
            continue

        # add to list if all condition passed
        candidates.append(m)
        
    return candidates