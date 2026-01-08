import requests
from typing import List
from ..core.models import MarketRecord
from ..core.parse import parse_market

class GammaClient:
    # a client to interact with Polymarket's Gamma API
    
    BASE_URL = "https://gamma-api.polymarket.com/markets"

    def fetch_markets(self, limit: int = 100, pages: int = 5) -> List[MarketRecord]:
        '''
        Fetches markets using pagination.
        
        Args:
            limit: How many markets to get per request
            pages: How many pages to fetch (total markets = limit * pages).
        '''

        all_records = []
        
        print(f"Fetching {pages} pages of markets...")

        for page in range(pages):
            offset = page * limit
            try:
                # Define parameters for the API call
                params = {
                    "limit": limit,
                    "offset": offset,
                    "active": "true",          
                    "closed": "false",         
                    "enableOrderBook": "true",
                    "order": "volume",
                    "ascending": "false"       
                }
                
                # send the request
                response = requests.get(self.BASE_URL, params=params, timeout=10)
                response.raise_for_status() # Check for http errors 
                
                data = response.json()
                
                # If list is empty, means it reached the end
                if not data:
                    break

                # Convert raw dictionaries into MarketRecord objects
                for raw_item in data:
                    record = parse_market(raw_item)
                    all_records.append(record)

            except Exception as e:
                print(f"Error fetching page {page}: {e}")
                continue # continue to next page instead of crashing
                
        print(f"Successfully loaded {len(all_records)} raw market records.")
        return all_records