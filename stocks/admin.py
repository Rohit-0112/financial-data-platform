from django.contrib import admin
from .models import Company, StockData

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['symbol', 'name', 'sector']
    search_fields = ['symbol', 'name']

@admin.register(StockData)
class StockDataAdmin(admin.ModelAdmin):
    list_display = ['company', 'date', 'close_price', 'daily_return', 'volume']
    list_filter = ['company', 'date']
    date_hierarchy = 'date'