from django.db import models

class ForecastResult(models.Model):
    """Модель для хранения результата прогнозирования Prophet."""
    
    # Дата, на которую сделан прогноз (т.е. на 7 дней вперед)
    forecast_date = models.DateField(unique=True) 
    
    # Прогнозируемая цена (yhat)
    forecast_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Нижняя граница доверительного интервала (yhat_lower)
    lower_bound = models.DecimalField(max_digits=10, decimal_places=2) 
    
    # Верхняя граница доверительного интервала (yhat_upper)
    upper_bound = models.DecimalField(max_digits=10, decimal_places=2) 
    
    # Дата, когда прогноз был выполнен (для истории)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Прогноз ETH на {self.forecast_date}: ${self.forecast_price}"

    class Meta:
        ordering = ['-forecast_date']