from rest_framework import serializers
from .models import Company, StockData


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['symbol', 'name', 'sector', 'description']


class StockDataSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)
    company_symbol = serializers.CharField(source='company.symbol', read_only=True)

    class Meta:
        model = StockData
        fields = [
            'id', 'company_name', 'company_symbol', 'date',
            'open_price', 'high_price', 'low_price', 'close_price', 'volume',
            'daily_return', 'moving_avg_7', 'week_52_high', 'week_52_low',
            'volatility_score', 'momentum'
        ]


class StockSummarySerializer(serializers.Serializer):
    symbol = serializers.CharField()
    name = serializers.CharField()
    current_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    week_52_high = serializers.DecimalField(max_digits=10, decimal_places=2)
    week_52_low = serializers.DecimalField(max_digits=10, decimal_places=2)
    average_close = serializers.DecimalField(max_digits=10, decimal_places=2)
    last_updated = serializers.DateField()


class ComparisonSerializer(serializers.Serializer):
    symbol1 = serializers.CharField()
    symbol2 = serializers.CharField()
    comparison_data = serializers.DictField()