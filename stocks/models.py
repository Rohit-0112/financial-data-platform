from django.db import models


class Company(models.Model):
    symbol = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=100)
    sector = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.symbol} - {self.name}"


class StockData(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    date = models.DateField()
    open_price = models.DecimalField(max_digits=10, decimal_places=2)
    high_price = models.DecimalField(max_digits=10, decimal_places=2)
    low_price = models.DecimalField(max_digits=10, decimal_places=2)
    close_price = models.DecimalField(max_digits=10, decimal_places=2)
    volume = models.BigIntegerField()

    # Calculated fields
    daily_return = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    moving_avg_7 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    week_52_high = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    week_52_low = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Creative metrics
    volatility_score = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    momentum = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)

    class Meta:
        unique_together = ['company', 'date']
        ordering = ['-date']

    def __str__(self):
        return f"{self.company.symbol} - {self.date} - ₹{self.close_price}"