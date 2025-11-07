import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from stocks.models import Company, StockData


class StockDataCollector:
    # Indian stock symbols (NSE)
    # US stock symbols (more reliable with yfinance)
    US_STOCKS = {
        'AAPL': 'Apple Inc.',
        'GOOGL': 'Alphabet Inc. (Google)',
        'MSFT': 'Microsoft Corporation',
        'TSLA': 'Tesla Inc.',
        'AMZN': 'Amazon.com Inc.',
        'META': 'Meta Platforms Inc. (Facebook)',
        'NFLX': 'Netflix Inc.',
        'NVDA': 'NVIDIA Corporation',
        'JPM': 'JPMorgan Chase & Co.',
        'JNJ': 'Johnson & Johnson'
    }

    @classmethod
    def setup_companies(cls):
        """Create Company objects in database"""
        for symbol, name in cls.US_STOCKS.items():
            company, created = Company.objects.get_or_create(
                symbol=symbol,
                defaults={
                    'name': name,
                    'sector': 'Various'
                }
            )
            if created:
                print(f"Created company: {name}")

    @classmethod
    def fetch_stock_data(cls, symbol, period="1y"):
        """Fetch stock data from Yahoo Finance"""
        try:
            stock = yf.Ticker(symbol)
            hist_data = stock.history(period=period)

            if hist_data.empty:
                print(f"No data found for {symbol}")
                return None

            return hist_data
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
            return None

    @classmethod
    def calculate_metrics(cls, df):
        """Calculate financial metrics"""
        df = df.copy()

        # Daily Return
        df['daily_return'] = (df['Close'] - df['Open']) / df['Open']

        # 7-day Moving Average
        df['moving_avg_7'] = df['Close'].rolling(window=7).mean()

        # 52-week High/Low (rolling 252 trading days)
        df['week_52_high'] = df['High'].rolling(window=252).max()
        df['week_52_low'] = df['Low'].rolling(window=252).min()

        # Creative Metrics
        # Volatility Score (30-day standard deviation of returns)
        df['volatility_score'] = df['daily_return'].rolling(window=30).std() * 100

        # Momentum (price change over 20 days)
        df['momentum'] = (df['Close'] - df['Close'].shift(20)) / df['Close'].shift(20) * 100

        return df

    @classmethod
    def save_stock_data(cls, symbol, df):
        """Save processed data to database"""
        company = Company.objects.get(symbol=symbol)

        records_created = 0
        for date, row in df.iterrows():
            # Skip if any essential data is missing
            if pd.isna(row['Close']) or pd.isna(row['Open']):
                continue

            stock_data, created = StockData.objects.update_or_create(
                company=company,
                date=date.date(),
                defaults={
                    'open_price': round(float(row['Open']), 2),
                    'high_price': round(float(row['High']), 2),
                    'low_price': round(float(row['Low']), 2),
                    'close_price': round(float(row['Close']), 2),
                    'volume': int(row['Volume']),
                    'daily_return': round(float(row.get('daily_return', 0)), 4),
                    'moving_avg_7': round(float(row.get('moving_avg_7', 0)), 2),
                    'week_52_high': round(float(row.get('week_52_high', 0)), 2),
                    'week_52_low': round(float(row.get('week_52_low', 0)), 2),
                    'volatility_score': round(float(row.get('volatility_score', 0)), 4),
                    'momentum': round(float(row.get('momentum', 0)), 4),
                }
            )

            if created:
                records_created += 1

        return records_created

    @classmethod
    def collect_all_data(cls):
        """Main method to collect all stock data"""
        print("Setting up companies...")
        cls.setup_companies()

        for symbol in cls.INDIAN_STOCKS.keys():
            print(f"Fetching data for {symbol}...")

            # Fetch raw data
            raw_data = cls.fetch_stock_data(symbol, period="2y")  # 2 years for 52-week calc

            if raw_data is not None:
                # Calculate metrics
                processed_data = cls.calculate_metrics(raw_data)

                # Save to database
                records_created = cls.save_stock_data(symbol, processed_data)
                print(f"Created {records_created} records for {symbol}")
            else:
                print(f"Failed to fetch data for {symbol}")

        print("Data collection completed!")