class StockDashboard {
    constructor() {
        this.currentCompany = null;
        this.companies = [];
        this.priceChart = null;
        this.performanceChart = null;
        this.comparisonChart = null;

        this.init();
    }

    async init() {
        await this.loadCompanies();
        this.setupEventListeners();
        this.setupComparisonSelects();
    }

    async loadCompanies() {
        try {
            const response = await fetch('/stocks/api/companies/');
            this.companies = await response.json();
            this.renderCompaniesList();
            this.populateComparisonSelects();
        } catch (error) {
            console.error('Error loading companies:', error);
        }
    }

    renderCompaniesList() {
        const companiesList = document.getElementById('companiesList');
        companiesList.innerHTML = '';

        this.companies.forEach(company => {
            const companyElement = document.createElement('div');
            companyElement.className = 'company-item p-2 mb-1 rounded';
            companyElement.innerHTML = `
                <strong>${company.symbol}</strong>
                <br>
                <small class="text-muted">${company.name}</small>
            `;
            companyElement.addEventListener('click', () => this.selectCompany(company));
            companiesList.appendChild(companyElement);
        });
    }

    async selectCompany(company) {
        // Update UI
        document.querySelectorAll('.company-item').forEach(item => item.classList.remove('active'));
        event.currentTarget.classList.add('active');

        this.currentCompany = company;

        // Show company info
        document.getElementById('companyInfo').style.display = 'block';
        document.getElementById('companyName').textContent = company.name;
        document.getElementById('companySymbol').textContent = company.symbol;

        // Load company data
        await this.loadCompanyData(company.symbol);
        await this.loadCompanySummary(company.symbol);
    }

    async loadCompanyData(symbol) {
        try {
            const response = await fetch(`/stocks/api/data/${symbol}/`);
            const data = await response.json();

            this.renderPriceChart(data);
            this.renderPerformanceChart(data);
        } catch (error) {
            console.error('Error loading company data:', error);
        }
    }

    async loadCompanySummary(symbol) {
        try {
            const response = await fetch(`/stocks/api/summary/${symbol}/`);
            const summary = await response.json();

            this.updateCompanyInfo(summary);
            this.renderKeyMetrics(summary);
        } catch (error) {
            console.error('Error loading company summary:', error);
        }
    }

    renderPriceChart(stockData) {
        const ctx = document.getElementById('priceChart').getContext('2d');

        // Destroy existing chart
        if (this.priceChart) {
            this.priceChart.destroy();
        }

        const dates = stockData.map(item => new Date(item.date).toLocaleDateString()).reverse();
        const prices = stockData.map(item => parseFloat(item.close_price)).reverse();

        this.priceChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: dates,
                datasets: [{
                    label: 'Closing Price',
                    data: prices,
                    borderColor: '#007bff',
                    backgroundColor: 'rgba(0, 123, 255, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: '30-Day Price History'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: false
                    }
                }
            }
        });
    }

    renderPerformanceChart(stockData) {
        const ctx = document.getElementById('performanceChart').getContext('2d');

        if (this.performanceChart) {
            this.performanceChart.destroy();
        }

        const returns = stockData.map(item => parseFloat(item.daily_return) * 100).reverse();
        const colors = returns.map(r => r >= 0 ? '#28a745' : '#dc3545');

        this.performanceChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: returns.map((_, i) => i + 1 + 'd ago'),
                datasets: [{
                    label: 'Daily Return (%)',
                    data: returns,
                    backgroundColor: colors,
                    borderColor: colors,
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }

    updateCompanyInfo(summary) {
        document.getElementById('currentPrice').textContent = `$${parseFloat(summary.current_price).toFixed(2)}`;

        // Calculate daily change (you might want to get this from the latest data)
        const changePercent = 0; // This should come from your data
        const changeElement = document.getElementById('priceChange');
        changeElement.textContent = `${changePercent >= 0 ? '+' : ''}${changePercent.toFixed(2)}% Today`;
        changeElement.className = changePercent >= 0 ? 'text-success' : 'text-danger';
    }

    renderKeyMetrics(summary) {
        const metricsContainer = document.getElementById('keyMetrics');
        metricsContainer.innerHTML = `
            <div class="row text-center">
                <div class="col-6 mb-3">
                    <div class="card stock-card">
                        <div class="card-body">
                            <h6 class="card-title">52-Week High</h6>
                            <h5 class="text-success">$${parseFloat(summary.week_52_high).toFixed(2)}</h5>
                        </div>
                    </div>
                </div>
                <div class="col-6 mb-3">
                    <div class="card stock-card">
                        <div class="card-body">
                            <h6 class="card-title">52-Week Low</h6>
                            <h5 class="text-danger">$${parseFloat(summary.week_52_low).toFixed(2)}</h5>
                        </div>
                    </div>
                </div>
                <div class="col-6 mb-3">
                    <div class="card stock-card">
                        <div class="card-body">
                            <h6 class="card-title">Avg Price</h6>
                            <h5 class="text-primary">$${parseFloat(summary.average_close).toFixed(2)}</h5>
                        </div>
                    </div>
                </div>
                <div class="col-6 mb-3">
                    <div class="card stock-card">
                        <div class="card-body">
                            <h6 class="card-title">Last Updated</h6>
                            <h6>${new Date(summary.last_updated).toLocaleDateString()}</h6>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    setupComparisonSelects() {
        document.getElementById('compareBtn').addEventListener('click', () => {
            const symbol1 = document.getElementById('compareSelect1').value;
            const symbol2 = document.getElementById('compareSelect2').value;

            if (symbol1 && symbol2) {
                this.compareStocks(symbol1, symbol2);
            }
        });
    }

    populateComparisonSelects() {
        const select1 = document.getElementById('compareSelect1');
        const select2 = document.getElementById('compareSelect2');

        this.companies.forEach(company => {
            const option1 = new Option(`${company.symbol} - ${company.name}`, company.symbol);
            const option2 = new Option(`${company.symbol} - ${company.name}`, company.symbol);

            select1.add(option1);
            select2.add(option2);
        });
    }

    async compareStocks(symbol1, symbol2) {
        try {
            const response = await fetch(`/stocks/api/compare/?symbol1=${symbol1}&symbol2=${symbol2}`);
            const comparison = await response.json();

            this.renderComparisonChart(comparison.comparison_data);
        } catch (error) {
            console.error('Error comparing stocks:', error);
        }
    }

    renderComparisonChart(comparisonData) {
        const ctx = document.getElementById('comparisonChart').getContext('2d');

        if (this.comparisonChart) {
            this.comparisonChart.destroy();
        }

        const symbols = Object.keys(comparisonData.performance);
        const returns = symbols.map(symbol => comparisonData.performance[symbol].avg_daily_return);
        const volatilities = symbols.map(symbol => comparisonData.performance[symbol].volatility_score);

        this.comparisonChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: symbols,
                datasets: [
                    {
                        label: 'Avg Daily Return (%)',
                        data: returns,
                        backgroundColor: 'rgba(54, 162, 235, 0.8)',
                        borderColor: 'rgba(54, 162, 235, 1)',
                        borderWidth: 1,
                        yAxisID: 'y'
                    },
                    {
                        label: 'Volatility Score',
                        data: volatilities,
                        backgroundColor: 'rgba(255, 99, 132, 0.8)',
                        borderColor: 'rgba(255, 99, 132, 1)',
                        borderWidth: 1,
                        yAxisID: 'y1'
                    }
                ]
            },
            options: {
                responsive: true,
                interaction: {
                    mode: 'index',
                    intersect: false,
                },
                scales: {
                    y: {
                        type: 'linear',
                        display: true,
                        position: 'left',
                        title: {
                            display: true,
                            text: 'Avg Daily Return (%)'
                        }
                    },
                    y1: {
                        type: 'linear',
                        display: true,
                        position: 'right',
                        title: {
                            display: true,
                            text: 'Volatility Score'
                        },
                        grid: {
                            drawOnChartArea: false,
                        },
                    }
                }
            }
        });
    }

    setupEventListeners() {
        // Search functionality
        document.getElementById('searchInput').addEventListener('input', (e) => {
            const searchTerm = e.target.value.toLowerCase();
            document.querySelectorAll('.company-item').forEach(item => {
                const text = item.textContent.toLowerCase();
                item.style.display = text.includes(searchTerm) ? 'block' : 'none';
            });
        });
    }
}

// Initialize dashboard when page loads
document.addEventListener('DOMContentLoaded', () => {
    new StockDashboard();
});