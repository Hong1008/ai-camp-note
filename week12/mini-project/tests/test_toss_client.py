import unittest
from unittest.mock import patch, MagicMock
import json
import os
import sys
import time
from pathlib import Path

# Add project directories to Python path
sys.path.append(str(Path(__file__).resolve().parents[1]))
sys.path.append(str(Path(__file__).resolve().parents[3]))

import config
from toss_client import TossClient

class TestTossClient(unittest.TestCase):
    
    def setUp(self):
        # Temp credentials for test
        self.api_key = "test_key"
        self.secret_key = "test_secret"
        
        # Override config credentials just in case
        config.TOSS_API_KEY = self.api_key
        config.TOSS_SECRET_KEY = self.secret_key
        
        self.client = TossClient(self.api_key, self.secret_key)
        # Clear token file cache if it exists
        if self.client.TOKEN_CACHE_FILE.exists():
            os.remove(self.client.TOKEN_CACHE_FILE)

    def tearDown(self):
        # Clean up files
        if self.client.TOKEN_CACHE_FILE.exists():
            os.remove(self.client.TOKEN_CACHE_FILE)

    @patch("requests.post")
    def test_token_caching_and_retrieval(self, mock_post):
        # Mock token response
        mock_res = MagicMock()
        mock_res.status_code = 200
        mock_res.json.return_value = {
            "access_token": "mock_jwt_token_xyz",
            "token_type": "Bearer",
            "expires_in": 3600
        }
        mock_post.return_value = mock_res
        
        # 1. First retrieval should call requests.post
        token = self.client.get_access_token()
        self.assertEqual(token, "mock_jwt_token_xyz")
        self.assertTrue(self.client.TOKEN_CACHE_FILE.exists())
        mock_post.assert_called_once()
        
        # Reset mock call count
        mock_post.reset_mock()
        
        # 2. Second retrieval should load from memory cache (no requests.post)
        token2 = self.client.get_access_token()
        self.assertEqual(token2, "mock_jwt_token_xyz")
        mock_post.assert_not_called()
        
        # 3. Clear memory cache, should load from file cache (no requests.post)
        self.client._access_token = None
        self.client._token_expires_at = 0
        token3 = self.client.get_access_token()
        self.assertEqual(token3, "mock_jwt_token_xyz")
        mock_post.assert_not_called()

    @patch("requests.post")
    @patch("requests.get")
    def test_get_prices(self, mock_get, mock_post):
        # Mock token response
        mock_token_res = MagicMock()
        mock_token_res.status_code = 200
        mock_token_res.json.return_value = {
            "access_token": "mock_jwt_token",
            "expires_in": 3600
        }
        mock_post.return_value = mock_token_res
        
        # Mock prices response
        mock_prices_res = MagicMock()
        mock_prices_res.status_code = 200
        mock_prices_res.json.return_value = {
            "result": [
                {"symbol": "005930", "lastPrice": "72000", "currency": "KRW"},
                {"symbol": "000660", "lastPrice": "180000", "currency": "KRW"}
            ]
        }
        mock_get.return_value = mock_prices_res
        
        prices = self.client.get_prices(["005930", "000660"])
        self.assertEqual(len(prices), 2)
        self.assertEqual(prices[0]["symbol"], "005930")
        self.assertEqual(prices[0]["lastPrice"], "72000")
        
        mock_get.assert_called_once_with(
            "https://openapi.tossinvest.com/api/v1/prices",
            headers={"Authorization": "Bearer mock_jwt_token", "Content-Type": "application/json"},
            params={"symbols": "005930,000660"}
        )

    @patch("requests.post")
    @patch("requests.get")
    def test_get_candles(self, mock_get, mock_post):
        mock_token_res = MagicMock()
        mock_token_res.status_code = 200
        mock_token_res.json.return_value = {"access_token": "mock_jwt_token", "expires_in": 3600}
        mock_post.return_value = mock_token_res
        
        mock_candles_res = MagicMock()
        mock_candles_res.status_code = 200
        mock_candles_res.json.return_value = {
            "result": {
                "candles": [
                    {"timestamp": "2026-03-25T09:00:00+09:00", "closePrice": "72000"}
                ]
            }
        }
        mock_get.return_value = mock_candles_res
        
        res = self.client.get_candles("005930", "1d", 10)
        self.assertIn("candles", res)
        self.assertEqual(res["candles"][0]["closePrice"], "72000")

if __name__ == "__main__":
    unittest.main()
