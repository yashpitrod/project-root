import requests
from datetime import datetime

class CurrentRatesCollector:
    def __init__(self):
        # Fallback values (used if API fails)
        self.fallback_data = {
            "fd_rates": {"SBI": 6.5, "HDFC": 7.1, "ICICI": 6.9},
            "gold_price": 6200,   # per gram (24k INR)
            "inflation": 6.8,     # CPI inflation %
            "repo_rate": 6.5
        }

    def get_fd_rates(self):
        """Fetch FD rates (simulated API / manual update)."""
        try:
            # Example: RBI or bank FD API (not public → so we simulate here)
            # Replace with scraping if allowed
            return {"SBI": 6.75, "HDFC": 7.25, "ICICI": 7.0}
        except Exception:
            return self.fallback_data["fd_rates"]

    def get_gold_price(self):
        """Fetch live gold price per gram (INR)."""
        try:
            # Example API (GoldAPI.io → needs API key)
            url = "https://www.goldapi.io/api/XAU/INR"
            headers = {"x-access-token": "goldapi-your-api-key"}
            res = requests.get(url, headers=headers, timeout=5)
            if res.status_code == 200:
                data = res.json()
                return round(data["price"] / 31.1035)  # per gram from per ounce
            return self.fallback_data["gold_price"]
        except Exception:
            return self.fallback_data["gold_price"]

    def get_inflation_rate(self):
        """Fetch latest CPI inflation (India)."""
        try:
            # MOSPI or TradingEconomics API
            url = "https://api.tradingeconomics.com/india/inflation?c=guest:guest"
            res = requests.get(url, timeout=5)
            if res.status_code == 200:
                data = res.json()
                return round(data[0]["Value"], 2)
            return self.fallback_data["inflation"]
        except Exception:
            return self.fallback_data["inflation"]

    def get_repo_rate(self):
        """Fetch RBI repo rate."""
        try:
            url = "https://api.tradingeconomics.com/india/interestrate?c=guest:guest"
            res = requests.get(url, timeout=5)
            if res.status_code == 200:
                data = res.json()
                return round(data[0]["Value"], 2)
            return self.fallback_data["repo_rate"]
        except Exception:
            return self.fallback_data["repo_rate"]

    def collect_all_current_data(self):
        """Return dictionary of latest financial data."""
        return {
            "fd_rates": self.get_fd_rates(),
            "gold_price": self.get_gold_price(),
            "inflation": self.get_inflation_rate(),
            "repo_rate": self.get_repo_rate(),
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
