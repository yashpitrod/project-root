import yfinance as yf
import pandas as pd
import requests
import json
from datetime import datetime, timedelta
from config import Config

class FinancialDataCollector:
    def __init__(self):
        self.config = Config()
        self.market_data = {}
        self.fd_rates = {}
        
    def collect_indian_market_data(self):
        """Collect Indian market data including Nifty, Sensex, major stocks"""
        print("📈 Collecting Indian market data...")
        
        # Indian market symbols
        indian_symbols = [
            '^NSEI',      # Nifty 50
            '^BSESN',     # BSE Sensex
            'RELIANCE.NS', 'TCS.NS', 'INFY.NS', 'HDFC.NS',
            'ICICIBANK.NS', 'KOTAKBANK.NS', 'SBIN.NS', 'ITC.NS'
        ]
        
        # Gold and commodity symbols
        commodity_symbols = ['GC=F', 'GOLD', 'SI=F']  # Gold and Silver
        
        all_symbols = indian_symbols + commodity_symbols
        
        for symbol in all_symbols:
            try:
                print(f"Fetching data for {symbol}...")
                ticker = yf.Ticker(symbol)
                
                # Get 2 years of historical data
                hist = ticker.history(period="2y")
                
                if not hist.empty:
                    self.market_data[symbol] = {
                        'prices': hist,
                        'info': ticker.info,
                        'last_price': hist['Close'].iloc[-1],
                        'returns': hist['Close'].pct_change().dropna()
                    }
                    
            except Exception as e:
                print(f"Error fetching {symbol}: {e}")
                continue
        
        print(f"✅ Collected data for {len(self.market_data)} symbols")
        return self.market_data
    
    def collect_fd_rates(self):
        """Collect Fixed Deposit rates from major Indian banks"""
        print("🏦 Collecting FD rates...")
        
        # Sample FD rates (in real implementation, scrape from bank websites)
        self.fd_rates = {
            'SBI': {
                '1_year': 6.7, '2_year': 6.9, '3_year': 6.9, '5_year': 6.5
            },
            'HDFC': {
                '1_year': 7.0, '2_year': 7.1, '3_year': 7.1, '5_year': 6.8
            },
            'ICICI': {
                '1_year': 7.0, '2_year': 7.1, '3_year': 7.1, '5_year': 6.8
            },
            'Axis': {
                '1_year': 7.25, '2_year': 7.25, '3_year': 7.0, '5_year': 6.75
            },
            'Kotak': {
                '1_year': 7.0, '2_year': 7.0, '3_year': 6.5, '5_year': 6.5
            }
        }
        
        print("✅ FD rates collected")
        return self.fd_rates
    
    def get_current_inflation_rate(self):
        """Get current inflation rate (sample data)"""
        return 6.2  # Current India inflation rate
    
    def save_data(self, filename):
        """Save collected data to file"""
        data_to_save = {
            'market_data': {k: {
                'last_price': float(v['last_price']),
                'avg_return': float(v['returns'].mean() * 252),  # Annualized
                'volatility': float(v['returns'].std() * (252**0.5))  # Annualized
            } for k, v in self.market_data.items()},
            'fd_rates': self.fd_rates,
            'inflation_rate': self.get_current_inflation_rate(),
            'collection_date': datetime.now().isoformat()
        }
        
        with open(f"{self.config.DATA_DIR}/{filename}", 'w') as f:
            json.dump(data_to_save, f, indent=2)
        
        print(f"💾 Data saved to {filename}")

if __name__ == "__main__":
    collector = FinancialDataCollector()
    collector.collect_indian_market_data()
    collector.collect_fd_rates()
    collector.save_data('financial_data.json')