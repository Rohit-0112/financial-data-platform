from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Avg, Max, Min
from .models import Company, StockData
from .serializers import *


@api_view(['GET'])
def companies_list(request):
    """Returns a list of all available companies"""
    companies = Company.objects.all()
    serializer = CompanySerializer(companies, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def stock_data(request, symbol):
    """Returns last 30 days of stock data for a company"""
    try:
        company = Company.objects.get(symbol=symbol)
        stock_data = StockData.objects.filter(company=company).order_by('-date')[:30]
        serializer = StockDataSerializer(stock_data, many=True)
        return Response(serializer.data)
    except Company.DoesNotExist:
        return Response(
            {"error": f"Company with symbol '{symbol}' not found"},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
def stock_summary(request, symbol):
    """Returns 52-week high, low, and average close"""
    try:
        company = Company.objects.get(symbol=symbol)

        # Get the latest stock data
        latest_data = StockData.objects.filter(company=company).order_by('-date').first()

        if not latest_data:
            return Response(
                {"error": f"No data available for '{symbol}'"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Calculate summary statistics
        stock_data = StockData.objects.filter(company=company)

        summary_data = {
            'symbol': company.symbol,
            'name': company.name,
            'current_price': latest_data.close_price,
            'week_52_high': stock_data.aggregate(Max('week_52_high'))['week_52_high__max'],
            'week_52_low': stock_data.aggregate(Min('week_52_low'))['week_52_low__min'],
            'average_close': stock_data.aggregate(Avg('close_price'))['close_price__avg'],
            'last_updated': latest_data.date
        }

        serializer = StockSummarySerializer(summary_data)
        return Response(serializer.data)

    except Company.DoesNotExist:
        return Response(
            {"error": f"Company with symbol '{symbol}' not found"},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
def compare_stocks(request):
    """Compare two stocks' performance (Bonus feature)"""
    symbol1 = request.GET.get('symbol1')
    symbol2 = request.GET.get('symbol2')

    if not symbol1 or not symbol2:
        return Response(
            {"error": "Please provide both symbol1 and symbol2 parameters"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        company1 = Company.objects.get(symbol=symbol1)
        company2 = Company.objects.get(symbol=symbol2)

        # Get last 30 days data for both companies
        data1 = StockData.objects.filter(company=company1).order_by('-date')[:30]
        data2 = StockData.objects.filter(company=company2).order_by('-date')[:30]

        # Calculate comparison metrics
        avg_return1 = data1.aggregate(Avg('daily_return'))['daily_return__avg'] or 0
        avg_return2 = data2.aggregate(Avg('daily_return'))['daily_return__avg'] or 0

        volatility1 = data1.aggregate(Avg('volatility_score'))['volatility_score__avg'] or 0
        volatility2 = data2.aggregate(Avg('volatility_score'))['volatility_score__avg'] or 0

        comparison_data = {
            'companies': {
                symbol1: CompanySerializer(company1).data,
                symbol2: CompanySerializer(company2).data
            },
            'performance': {
                symbol1: {
                    'avg_daily_return': round(float(avg_return1) * 100, 2),  # as percentage
                    'volatility_score': round(float(volatility1), 2),
                    'current_price': data1.first().close_price if data1 else 0
                },
                symbol2: {
                    'avg_daily_return': round(float(avg_return2) * 100, 2),
                    'volatility_score': round(float(volatility2), 2),
                    'current_price': data2.first().close_price if data2 else 0
                }
            },
            'comparison': {
                'higher_return': symbol1 if avg_return1 > avg_return2 else symbol2,
                'lower_volatility': symbol1 if volatility1 < volatility2 else symbol2,
                'return_difference': round(abs(avg_return1 - avg_return2) * 100, 2)
            }
        }

        serializer = ComparisonSerializer({
            'symbol1': symbol1,
            'symbol2': symbol2,
            'comparison_data': comparison_data
        })

        return Response(serializer.data)

    except Company.DoesNotExist:
        return Response(
            {"error": "One or both companies not found"},
            status=status.HTTP_404_NOT_FOUND
        )


# Creative Bonus API - Stock Insights
@api_view(['GET'])
def stock_insights(request, symbol):
    """Creative endpoint: Provides insights and analysis for a stock"""
    try:
        company = Company.objects.get(symbol=symbol)
        stock_data = StockData.objects.filter(company=company).order_by('-date')[:60]  # Last 60 days

        if not stock_data:
            return Response(
                {"error": f"No data available for '{symbol}'"},
                status=status.HTTP_404_NOT_FOUND
            )

        latest = stock_data.first()

        # Calculate insights
        positive_days = sum(1 for data in stock_data if data.daily_return > 0)
        negative_days = sum(1 for data in stock_data if data.daily_return < 0)

        # Trend analysis (simple)
        recent_trend = "Bullish" if latest.daily_return > 0 else "Bearish"

        # Volatility assessment
        avg_volatility = stock_data.aggregate(Avg('volatility_score'))['volatility_score__avg'] or 0
        volatility_level = "High" if avg_volatility > 2 else "Low" if avg_volatility < 1 else "Medium"

        insights = {
            'symbol': company.symbol,
            'name': company.name,
            'current_price': latest.close_price,
            'insights': {
                'trend': recent_trend,
                'volatility_level': volatility_level,
                'positive_days_ratio': f"{positive_days}/{len(stock_data)}",
                'performance_rating': "Good" if latest.daily_return > 0.01 else "Neutral" if latest.daily_return > -0.01 else "Poor",
                'momentum_strength': "Strong" if abs(latest.momentum or 0) > 5 else "Weak",
                'recommendation': "Watch" if volatility_level == "High" else "Consider" if latest.daily_return > 0 else "Hold"
            },
            'key_metrics': {
                'daily_change_percent': round(float(latest.daily_return or 0) * 100, 2),
                'volume_today': latest.volume,
                'distance_from_52_week_high': round(
                    float(((latest.week_52_high or 0) - latest.close_price) / (latest.week_52_high or 1) * 100), 2),
                'moving_avg_trend': "Above MA" if latest.close_price > (latest.moving_avg_7 or 0) else "Below MA"
            }
        }

        return Response(insights)

    except Company.DoesNotExist:
        return Response(
            {"error": f"Company with symbol '{symbol}' not found"},
            status=status.HTTP_404_NOT_FOUND
        )