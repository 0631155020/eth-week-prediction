import pandas as pd
import yfinance as yf
from prophet import Prophet
from datetime import date, timedelta
import warnings

# Отключаем предупреждения, чтобы вывод был чистым
warnings.filterwarnings('ignore')

# -----------------
# 1. Сбор данных
# -----------------
def fetch_data(ticker='ETH-USD', period='2y'):
    """Получает исторические данные о цене Ethereum."""
    print(f"-> Загрузка данных для {ticker} за последние {period}...")
    try:
        data = yf.download(ticker, period=period)
        
        # Prophet требует столбцы 'ds' (дата) и 'y' (значение)
        df = data.reset_index()
        df = df[['Date', 'Close']]
        df.columns = ['ds', 'y']
        
        # Конвертируем дату в формат Prophet
        df['ds'] = df['ds'].dt.date
        print(f"-> Загружено {len(df)} дней данных.")
        return df
    except Exception as e:
        print(f"Ошибка при загрузке данных: {e}")
        return pd.DataFrame()

# -----------------
# 2. Обучение и предсказание
# -----------------
def predict_price(df, days=7):
    """Обучает модель Prophet и делает предсказание."""
    
    # Инициализация и обучение модели
    # Настраиваем Prophet, который хорошо работает с сезонностью и трендами
    model = Prophet(
        daily_seasonality=True,
        weekly_seasonality=True,
        yearly_seasonality=True,
        seasonality_mode='multiplicative'
    )
    
    model.fit(df)
    print("-> Модель Prophet обучена.")

    # Создание фрейма данных для прогноза (на 7 дней вперед)
    future = model.make_future_dataframe(periods=days)
    
    # Предсказание
    forecast = model.predict(future)
    
    # Извлечение результата (прогноз на последний день)
    prediction_date = date.today() + timedelta(days=days)
    
    # Находим прогноз на нужную дату
    final_prediction = forecast[forecast['ds'] == str(prediction_date)]
    
    if final_prediction.empty:
        return None, None
    
    # yhat - это сам прогноз, yhat_lower/upper - доверительный интервал
    price = final_prediction['yhat'].iloc[0]
    lower = final_prediction['yhat_lower'].iloc[0]
    upper = final_prediction['yhat_upper'].iloc[0]

    return price, lower, upper

# -----------------
# 3. Вывод
# -----------------
if __name__ == '__main__':
    
    df_eth = fetch_data()
    
    if not df_eth.empty:
        # Прогноз на 7 дней
        days_to_predict = 7
        predicted_price, lower_bound, upper_bound = predict_price(df_eth, days=days_to_predict)

        if predicted_price:
            print("\n" + "="*50)
            print(f"ПРОГНОЗ ЦЕНЫ ЭФИРА (ETH/USD) ЧЕРЕЗ {days_to_predict} ДНЕЙ:")
            print(f"Дата прогноза: {(date.today() + timedelta(days=days_to_predict)).strftime('%Y-%m-%d')}")
            print(f"Прогнозируемая цена (yhat): ${predicted_price:.2f}")
            print(f"Доверительный интервал (95%): от ${lower_bound:.2f} до ${upper_bound:.2f}")
            print("="*50)
        else:
            print("Не удалось получить финальный прогноз.")