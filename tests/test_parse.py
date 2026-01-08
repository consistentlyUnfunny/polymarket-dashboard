import unittest
from src.core.parse import parse_market, calculate_hours_left

class TestMarketParsing(unittest.TestCase):
    
    def setUp(self):
        self.valid_raw = {
            "id": "123",
            "question": "Will BTC hit 100k?",
            "category": "Crypto",
            "endDate": "2026-12-31T23:59:59Z",
            "outcomes": "[\"Yes\", \"No\"]",  # JSON String format
            "outcomePrices": "[\"0.60\", \"0.40\"]",
            "clobTokenIds": "[\"token_yes\", \"token_no\"]",
            "enableOrderBook": True,
            "active": True
        }

    def test_parse_valid_json_strings(self):
        record = parse_market(self.valid_raw)
        
        self.assertEqual(record.question, "Will BTC hit 100k?")
        self.assertEqual(record.yes_price, 0.60)
        self.assertEqual(record.no_price, 0.40)
        self.assertEqual(record.yes_token_id, "token_yes")
        self.assertIsNone(record.invalid_reason)

    def test_parse_already_lists(self):
        raw = self.valid_raw.copy()
        raw["outcomes"] = ["Yes", "No"] # Not a string
        raw["outcomePrices"] = [0.55, 0.45]
        
        record = parse_market(raw)
        self.assertEqual(record.yes_price, 0.55)
        self.assertIsNone(record.invalid_reason)

    def test_invalid_non_binary_market(self):
        raw = self.valid_raw.copy()
        raw["outcomes"] = "[\"Yes\", \"No\", \"Maybe\"]"
        
        record = parse_market(raw)
        self.assertEqual(record.invalid_reason, "Not a binary market (must have 2 outcomes)")

    def test_time_calculation(self):
        # Future date
        hours = calculate_hours_left("2099-01-01T00:00:00Z")
        self.assertTrue(hours > 0)
        
        # Missing date
        hours = calculate_hours_left(None)
        self.assertEqual(hours, -1.0)

if __name__ == '__main__':
    unittest.main()