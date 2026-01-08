import requests
from typing import List, Dict

class ClobClient:
    #Client to interact with Polymarket's CLOB api
    
    BASE_URL = "https://clob.polymarket.com"

    def get_prices(self, token_ids: List[str]) -> Dict[str, float]:
        """
        Batches token IDs and fetches their latest mid-price.
        Returns a dict: {token_id: price}
        """
        if not token_ids:
            return {}

        results = {}
        chunk_size = 50
        
        for i in range(0, len(token_ids), chunk_size):
            chunk = token_ids[i:i + chunk_size]
            
            try:
                query_params = [{"token_id": t, "side": "buy"} for t in chunk]
                
                response = requests.post(
                    f"{self.BASE_URL}/prices", 
                    json=query_params, 
                    timeout=5
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    for t_id, price_data in data.items():
                        price = price_data.get("buy") or price_data.get("BUY")
                        
                        if price:
                            results[t_id] = float(price)
                            
            except Exception as e:
                print(f"CLOB fetch error: {e}")
                
        return results