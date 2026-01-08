# Defines the MarketRecord structure
from dataclasses import dataclass
from typing import Optional

# a dataclass to serve as the model for the market record
@dataclass
class MarketRecord:
    # basic info
    id: str
    question: str
    category: str
    slug: Optional[str] = None
    
    # time
    end_date_iso: Optional[str] = None
    hours_to_close: Optional[float] = None
    
    # status
    active: bool = False
    closed: bool = False
    enable_order_book: bool = False
    
    # prices and token data
    yes_token_id: Optional[str] = None
    no_token_id: Optional[str] = None
    yes_price: Optional[float] = None
    no_price: Optional[float] = None
    
    # for error tracking
    invalid_reason: Optional[str] = None

    def is_valid_candidate(self) -> bool:
        # Checks if market meets the core candidate criteria
        # Condtions: active, open, order book enabled, and have no data errors
        if self.invalid_reason:
            return False
            
        return (
            self.enable_order_book 
            and self.active 
            and not self.closed
        )