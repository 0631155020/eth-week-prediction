from django.shortcuts import render
from .utils import fetch_data, predict_price
from datetime import date, timedelta

def index(request):
    predicted_price = None
    lower_bound = None
    upper_bound = None
    prediction_date = None

    if request.method == 'POST':
        days_to_predict = int(request.POST.get('days', 7))
        df_eth = fetch_data()
        if not df_eth.empty:
            predicted_price, lower_bound, upper_bound = predict_price(df_eth, days=days_to_predict)
            prediction_date = (date.today() + timedelta(days=days_to_predict)).strftime('%Y-%m-%d')

    context = {
        'predicted_price': predicted_price,
        'lower_bound': lower_bound,
        'upper_bound': upper_bound,
        'prediction_date': prediction_date,
    }
    return render(request, 'prediction/index.html', context)