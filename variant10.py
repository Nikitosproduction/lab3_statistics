# Вариант 10: анализ инфляции в России
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

class InflationAnalysis:
    def __init__(self, filepath):
        self.df = pd.read_csv(filepath)
        self.df['year'] = pd.to_numeric(self.df['year'])
        self.df['inflation'] = pd.to_numeric(self.df['inflation'])

    def get_table_data(self):
        return self.df.values.tolist(), self.df.columns.tolist()

    def plot_data(self, ax):
        ax.plot(self.df['year'], self.df['inflation'], 'o-', label='Инфляция', color='green')
        ax.set_title('Инфляция в России')
        ax.set_xlabel('Год')
        ax.set_ylabel('Инфляция (%)')
        ax.grid(True, linestyle='--', alpha=0.6)
        ax.legend()

    def calculate_price_forecast(self, current_price=100, n_periods=3, forecast_years=5):
        avg_inflation = self.df['inflation'].iloc[-n_periods:].mean() / 100
        prices = [current_price]
        for _ in range(forecast_years):
            prices.append(prices[-1] * (1 + avg_inflation))
        return prices[1:]

    def moving_average_forecast(self, n_periods=3, forecast_years=5):
        data = self.df['inflation'].values
        forecasts = []
        last_values = data[-n_periods:].tolist()
        last_year = self.df['year'].iloc[-1]
        for i in range(forecast_years):
            next_val = sum(last_values[-n_periods:]) / n_periods
            forecasts.append(next_val)
            last_values.append(next_val)
        forecast_years_list = [last_year + i + 1 for i in range(forecast_years)]
        return forecast_years_list, forecasts

    def plot_forecast(self, ax, n_periods, forecast_years):
        forecast_years_list, forecasts = self.moving_average_forecast(n_periods, forecast_years)
        full_years = list(self.df['year']) + forecast_years_list
        full_values = list(self.df['inflation']) + forecasts
        ax.plot(full_years, full_values, 'o-', label='Исторические данные', color='blue')
        ax.plot(forecast_years_list, forecasts, 'o-', label='Прогноз инфляции', color='red')
        ax.axvline(x=self.df['year'].iloc[-1], color='gray', linestyle='--', alpha=0.7)
        ax.set_title('Прогноз инфляции (скользящая средняя)')
        ax.set_xlabel('Год')
        ax.set_ylabel('Инфляция (%)')
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.6)
        return full_years, full_values
