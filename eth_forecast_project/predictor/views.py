from django.shortcuts import render
from .models import ForecastResult

def prediction_dashboard(request):
    """Отображает последний сохраненный прогноз."""
    
    # Получаем самый последний прогноз из базы данных
    try:
        latest_forecast = ForecastResult.objects.latest('forecast_date')
    except ForecastResult.DoesNotExist:
        latest_forecast = None

    context = {
        'forecast': latest_forecast,
    }
    return render(request, 'predictor/dashboard.html', context)