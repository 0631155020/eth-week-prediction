import pandas as pd
import yfinance as yf
from prophet import Prophet
from datetime import date, timedelta
import warnings
from django.core.management.base import BaseCommand
from predictor.models import ForecastResult

# Отключаем предупреждения
warnings.filterwarnings('ignore')

class Command(BaseCommand):
    help = 'Запускает сбор данных, обучение модели Prophet и сохранение прогноза в БД'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("-> Начало процесса прогнозирования..."))

        # 1. Сбор данных
        df_eth = self.fetch_data()

        if df_eth.empty:
            self.stdout.write(self.style.ERROR("! Не удалось получить данные. Процесс остановлен."))
            return

        # 2. Обучение и предсказание
        days_to_predict = 7
        predicted_price, lower_bound, upper_bound = self.predict_price(df_eth, days=days_to_predict)

        if not predicted_price:
            self.stdout.write(self.style.ERROR("! Не удалось получить прогноз. Процесс остановлен."))
            return

        # 3. Сохранение в базу данных
        forecast_date = date.today() + timedelta(days=days_to_predict)

        # Используем update_or_create для избежания дубликатов
        obj, created = ForecastResult.objects.update_or_create(
            forecast_date=forecast_date,
            defaults={
                'forecast_price': predicted_price,
                'lower_bound': lower_bound,
                'upper_bound': upper_bound
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f"-> Прогноз на {forecast_date} успешно создан."))
        else:
            self.stdout.write(self.style.SUCCESS(f"-> Прогноз на {forecast_date} успешно обновлен."))

        self.stdout.write(self.style.SUCCESS("="*50))
        self.stdout.write(f"ПРОГНОЗ ЦЕНЫ ЭФИРА (ETH/USD) ЧЕРЕЗ {days_to_predict} ДНЕЙ:")
        self.stdout.write(f"Дата прогноза: {forecast_date.strftime('%Y-%m-%d')}")
        self.stdout.write(f"Прогнозируемая цена: ${predicted_price:.2f}")
        self.stdout.write(f"Доверительный интервал: от ${lower_bound:.2f} до ${upper_bound:.2f}")
        self.stdout.write(self.style.SUCCESS("="*50))


    def fetch_data(self, ticker='ETH-USD', period='2y'):
        """Получает исторические данные о цене Ethereum."""
        self.stdout.write(f"-> Загрузка данных для {ticker} за последние {period}...")
        try:
            data = yf.download(ticker, period=period)
            df = data.reset_index()
            df = df[['Date', 'Close']]
            df.columns = ['ds', 'y']
            df['ds'] = df['ds'].dt.date
            self.stdout.write(f"-> Загружено {len(df)} дней данных.")
            return df
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Ошибка при загрузке данных: {e}"))
            return pd.DataFrame()


    def predict_price(self, df, days=7):
        """Обучает модель Prophet и делает предсказание."""
        model = Prophet(
            daily_seasonality=True,
            weekly_seasonality=True,
            yearly_seasonality=True,
            seasonality_mode='multiplicative'
        )
        model.fit(df)
        self.stdout.write("-> Модель Prophet обучена.")

        future = model.make_future_dataframe(periods=days)
        forecast = model.predict(future)

        prediction_date = date.today() + timedelta(days=days)
        final_prediction = forecast[forecast['ds'] == str(prediction_date)]

        if final_prediction.empty:
            return None, None, None

        price = final_prediction['yhat'].iloc[0]
        lower = final_prediction['yhat_lower'].iloc[0]
        upper = final_prediction['yhat_upper'].iloc[0]

        return price, lower, upper
