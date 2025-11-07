# 📈 Financial Data Platform

A comprehensive stock market analysis platform built with Django that demonstrates real-time data collection, REST API development, and interactive data visualization.

## ✨ Features

### Core Functionality
- **Real-time Stock Data Collection** - Automated data fetching from Yahoo Finance
- **RESTful API Ecosystem** - Complete API endpoints for stock data access
- **Interactive Dashboard** - Beautiful charts and visualizations with Chart.js
- **Stock Comparison** - Compare performance between multiple stocks
- **Data Analytics** - Calculated metrics and financial indicators

###  Technical Features
- **Django Backend** - Robust and scalable web framework
- **REST API** - Clean, documented API endpoints
- **SQLite Database** - Data persistence and management
- **Responsive Design** - Bootstrap-powered frontend
- **Data Processing** - Pandas for efficient data manipulation

##  Tech Stack

- **Backend**: Django 4.2.7, Django REST Framework
- **Frontend**: HTML5, CSS3, JavaScript, Chart.js, Bootstrap 5
- **Database**: SQLite
- **Data Processing**: Pandas, yfinance
- **API**: RESTful architecture

##  Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)
----------------------------------------------------------------------------------------------------------------------
### Installation & Setup

1. Clone the repository
   git clone <https://github.com/Rohit-0112/financial-data-platform>
   cd financial_platform
   Create and activate virtual environment

2.Create and activate virtual environment
    # Windows
    python -m venv financial_env
    financial_env\Scripts\activate
    
    # Mac/Linux
    python -m venv financial_env
    source financial_env/bin/activate

3.Install dependencies
    pip install -r requirements.txt

4. setup database
    python manage.py migrate

5. Run server
       python manage.py runserver
--------------------------------------------------------------------------------------------------------------------

>>API Endpoints
Endpoint	                                Method	Description
/stocks/api/companies/	                      GET	List all available companies
/stocks/api/data/{symbol}/	                  GET	Last 30 days of stock data
/stocks/api/summary/{symbol}/	              GET	52-week high, low, and average close
/stocks/api/compare/?symbol1=X&symbol2=Y   	  GET	Compare two stocks' performance
/stocks/api/insights/{symbol}/	              GET	Advanced insights and analysis

>> Data Processing & Logic

    Data Collection
    Source: Yahoo Finance API via yfinance library
    
    Frequency: Daily stock data
    
    Companies: 10 major US stocks (AAPL, GOOGL, MSFT, etc.)
    
    Historical Data: 2 years for comprehensive analysis
    
    Calculated Metrics
    Daily Return: (Close - Open) / Open
    
    7-Day Moving Average: Rolling average of closing prices
    
    52-Week High/Low: Maximum and minimum prices over 252 trading days
    
    Volatility Score: 30-day standard deviation of daily returns
    
    Momentum Indicator: 20-day price change percentage


    Data Collection → Yahoo Finance API → Raw Stock Data
>> DATA FLOW
 
        Data Processing → Pandas → Calculated Metrics
        
        Data Storage → Django Models → SQLite Database
        
        API Layer → Django REST Framework → JSON Endpoints
        
        Frontend → JavaScript/Chart.js → Interactive Visualizations

>> Dashboard Features

      > Interactive Elements
            Company Selection: Click any company in sidebar to view data
            
            Price Charts: Interactive line charts showing 30-day price history
            
            Performance Metrics: Daily returns visualization with color coding
            
            Comparison Tools: Multi-stock comparison with side-by-side analysis
            
            Search Functionality: Filter companies by name or symbol
      
      > Visual Components
            Price History Chart: Line chart showing closing prices
            
            Daily Returns Chart: Bar chart with color-coded positive/negative returns
            
            Key Metrics Display: 52-week high/low, average price, volatility
            
            Comparison Charts: Multi-dataset bar charts for stock comparison
