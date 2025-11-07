from django.core.management.base import BaseCommand
from stocks.services.data_collector import StockDataCollector


class Command(BaseCommand):
    help = 'Fetch and update stock market data'

    def handle(self, *args, **options):
        self.stdout.write('Starting stock data collection...')

        try:
            StockDataCollector.collect_all_data()
            self.stdout.write(
                self.style.SUCCESS('Successfully collected all stock data!')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error collecting stock data: {e}')
            )