from django.core.management.base import BaseCommand
from stocks.models import Company, StockData
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Add sample stock data for testing'

    def handle(self, *args, **options):
        # Create sample companies
        companies_data = [
            {'symbol': 'AAPL', 'name': 'Apple Inc.', 'sector': 'Technology'},
            {'symbol': 'GOOGL', 'name': 'Alphabet Inc.', 'sector': 'Technology'},
            {'symbol': 'MSFT', 'name': 'Microsoft Corporation', 'sector': 'Technology'},
            {'symbol': 'TSLA', 'name': 'Tesla Inc.', 'sector': 'Automotive'},
            {'symbol': 'AMZN', 'name': 'Amazon.com Inc.', 'sector': 'E-Commerce'},
        ]

        for company_data in companies_data:
            company, created = Company.objects.get_or_create(
                symbol=company_data['symbol'],
                defaults=company_data
            )
            if created:
                self.stdout.write(f"Created company: {company.name}")

        # Add sample stock data
        for company in Company.objects.all():
            base_price = random.uniform(100, 300)
            current_date = datetime.now().date()

            for i in range(100):  # Add 100 days of data
                date = current_date - timedelta(days=i)

                open_price = base_price + random.uniform(-10, 10)
                close_price = open_price + random.uniform(-5, 5)
                high_price = max(open_price, close_price) + random.uniform(0, 5)
                low_price = min(open_price, close_price) - random.uniform(0, 5)

                # Calculate some metrics
                daily_return = (close_price - open_price) / open_price

                StockData.objects.get_or_create(
                    company=company,
                    date=date,
                    defaults={
                        'open_price': round(open_price, 2),
                        'high_price': round(high_price, 2),
                        'low_price': round(low_price, 2),
                        'close_price': round(close_price, 2),
                        'volume': random.randint(1000000, 5000000),
                        'daily_return': round(daily_return, 4),
                        'moving_avg_7': round(close_price + random.uniform(-2, 2), 2),
                        'week_52_high': round(base_price * 1.2, 2),
                        'week_52_low': round(base_price * 0.8, 2),
                        'volatility_score': round(random.uniform(0.5, 3.0), 4),
                        'momentum': round(random.uniform(-10, 10), 4),
                    }
                )

            self.stdout.write(f"Added sample data for {company.name}")

        self.stdout.write(
            self.style.SUCCESS('Successfully added sample stock data!')
        )