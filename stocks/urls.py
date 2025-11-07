from django.urls import path
from . import api_views
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    # API Endpoints
    path('api/companies/', api_views.companies_list, name='api_companies'),
    path('api/data/<str:symbol>/', api_views.stock_data, name='api_stock_data'),
    path('api/summary/<str:symbol>/', api_views.stock_summary, name='api_stock_summary'),
    path('api/compare/', api_views.compare_stocks, name='api_compare'),
    path('api/insights/<str:symbol>/', api_views.stock_insights, name='api_insights'),
]