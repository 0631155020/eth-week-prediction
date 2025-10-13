# 🚀 ETHEREUM PREDICTION MODEL (Python + Docker)

## Project Overview

This project is a simple predictive model designed to forecast the price of **Ethereum (ETH) in US Dollars** over a short-term horizon (7 days).

The model is implemented in **Python** and utilizes the **`Prophet`** library for time series analysis. The entire project is **containerized with Docker** to ensure fast and uniform deployment in any environment.

---

## ⚙️ Technology Stack

* **Language:** Python 3.10+
* **Core ML Library:** **Prophet** (developed by Meta) — an additive regression model for time series forecasting.
* **Data Collection:** `yfinance` to fetch historical ETH/USD prices.
* **Deployment:** **Docker** — for environment isolation and instant startup.

---

## 🧠 Model Mechanics

The Prophet model decomposes historical data (using data from the past 2 years) into key components for the forecast:

1.  **Trend:** The long-term direction of the price movement.
2.  **Seasonality:** Regular cyclical patterns (daily, weekly, and yearly cycles).
3.  **Uncertainty:** The output provides not only a point prediction (`yhat`) but also a **95% confidence interval** for risk assessment.

---

## 🛠️ Startup Instructions (Docker)

You will need Docker installed to run this model.

### 1. Clone the Repository

```bash
git clone https://github.com/0631155020/eth-week-prediction.git
cd eth-prediction
