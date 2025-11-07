from django.shortcuts import render
from django.http import JsonResponse
from .models import Company, StockData


def dashboard(request):
    """Main dashboard view"""
    return render(request, 'stocks/dashboard.html')


def stock_list(request):
    """Simple view to display stocks"""
    companies = Company.objects.all()
    context = {
        'companies': companies
    }
    return render(request, 'stocks/stock_list.html', context)


def get_stock_data(request, symbol):
    """API endpoint to get stock data (for testing)"""
    try:
        company = Company.objects.get(symbol=symbol)
        stock_data = StockData.objects.filter(company=company).order_by('-date')[:10]

        data = []
        for stock in stock_data:
            data.append({
                'date': stock.date,
                'close': float(stock.close_price),
                'open': float(stock.open_price),
                'daily_return': float(stock.daily_return),
            })

        return JsonResponse({'data': data})
    except Company.DoesNotExist:
        return JsonResponse({'error': 'Company not found'}, status=404)