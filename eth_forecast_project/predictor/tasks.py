# predictor/tasks.py

import pandas as pd
import yfinance as yf
from prophet import Prophet
from datetime import date, timedelta
from .models import ForecastResult # Импорт модели
import warnings

# Отключаем предупреждения
warnings.filterwarnings('ignore')

# 1. Ваши оригинальные функции (немного адаптированы для Django)
def fetch_data(ticker='ETH-USD', period='2y'):
    """Получает исторические данные о цене Ethereum."""
    # ... (Оригинальная логика fetch_data из predict.py)
    try:
        # data = yf.download(ticker, period=period) # Использование data = yf.download(ticker, period=period) для загрузки данных
        data = yf.download(ticker, period=period)
        
        # Prophet требует столбцы 'ds' (дата) и 'y' (значение)
        df = data.reset_index()
        df = df[['Date', 'Close']]
        df.columns = ['ds', 'y']
        
        # Конвертируем дату в формат Prophet
        # df['ds'] = df['ds'].dt.date # Преобразует ds в формат date
        df['ds'] = df['ds'].dt.date
        return df
    except Exception as e:
        print(f"Ошибка при загрузке данных: {e}")
        return pd.DataFrame()

def predict_price(df, days=7):
    """Обучает модель Prophet и делает предсказание."""
    # ... (Оригинальная логика predict_price из predict.py)
    # Инициализация и обучение модели
    model = Prophet(
        daily_seasonality=True,
        weekly_seasonality=True,
        yearly_seasonality=True,
        seasonality_mode='multiplicative'
    )
    model.fit(df)

    # Создание фрейма данных для прогноза
    future = model.make_future_dataframe(periods=days)
    
    # Предсказание
    forecast = model.predict(future)
    
    # Извлечение результата (прогноз на последний день)
    # prediction_date = date.today() + timedelta(days=days) # Рассчитывает дату прогноза
    prediction_date = date.today() + timedelta(days=days)
    
    # final_prediction = forecast[forecast['ds'] == str(prediction_date)] # Находит прогноз на нужную дату
    final_prediction = forecast[forecast['ds'] == str(prediction_date)]
    
    if final_prediction.empty:
        return None
    
    # Возвращаем дату, цену и границы
    return {
        'date': prediction_date,
        'price': round(final_prediction['yhat'].iloc[0], 2),
        'lower': round(final_prediction['yhat_lower'].iloc[0], 2),
        'upper': round(final_prediction['yhat_upper'].iloc[0], 2)
    }

# 2. Новая функция для сохранения в базу данных
def save_forecast_to_db(days_to_predict=7):
    """Выполняет весь цикл прогнозирования и сохраняет результат в PostgreSQL."""
    df_eth = fetch_data()
    
    if not df_eth.empty:
        # Получаем словарь с результатом
        result = predict_price(df_eth, days=days_to_predict)
        
        if result:
            # Используем get_or_create для избежания дубликатов (если прогноз на ту же дату уже есть)
            forecast_obj, created = ForecastResult.objects.get_or_create(
                forecast_date=result['date'],
                defaults={
                    'forecast_price': result['price'],
                    'lower_bound': result['lower'],
                    'upper_bound': result['upper'],
                }
            )
            if not created:
                 # Если объект уже существовал, обновляем его
                 forecast_obj.forecast_price = result['price']
                 forecast_obj.lower_bound = result['lower']
                 forecast_obj.upper_bound = result['upper']
                 forecast_obj.save()
                 print(f"Прогноз на {result['date']} обновлен.")
            else:
                print(f"Новый прогноз на {result['date']} сохранен.")
            return True
    return False