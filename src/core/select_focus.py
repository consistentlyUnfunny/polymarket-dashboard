# Logic to pick the 1 Crypto + 1 Sports market

from typing import List, Optional, Tuple
from .models import MarketRecord

def is_crypto(market: MarketRecord) -> bool:
    # check if market is crypto related, using common words
    keywords = ["crypto", "bitcoin", "ethereum", "solana", "btc", "eth"]
    text = (market.category + " " + market.question).lower()
    return any(k in text for k in keywords)

def is_sports(market: MarketRecord) -> bool:
    # check if market is sport related
    keywords = ["sports", "nba", "nfl", "soccer", "football", "premier league"]
    text = (market.category + " " + market.question).lower()
    return any(k in text for k in keywords)

def select_focus_markets(candidates: List[MarketRecord]) -> Tuple[Optional[MarketRecord], Optional[MarketRecord]]:
    # select one crypto and sport market
    crypto_pick = None
    sports_pick = None

    for market in candidates:
        # Pick the first Crypto match we find
        if not crypto_pick and is_crypto(market):
            crypto_pick = market
        
        # Pick the first Sports match we find
        if not sports_pick and is_sports(market):
            sports_pick = market
            
        # Optimization: Stop early if we found both
        if crypto_pick and sports_pick:
            break
            
    return crypto_pick, sports_pick