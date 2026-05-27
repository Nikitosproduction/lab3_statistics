import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from tkinter import messagebox

class PopulationAnalysis:
    def __init__(self, filepath):
        self.df = pd.read_csv(filepath)
        self.df['year'] = pd.to_numeric(self.df['year'])
        self.df['population'] = pd.to_numeric(self.df['population'])

    def get_table_data(self):
        return self.df.values.tolist(), self.df.columns.tolist()

    def plot_data(self, ax):
        ax.plot(self.df['year'], self.df['population'], 'o-', label='Численность населения')
        ax.set_title('Численность населения России')
        ax.set_xlabel('Год')
        ax.set_ylabel('Численность')
        ax.grid(True, linestyle='--', alpha=0.6)
        ax.legend()

    def calculate_max_min_change(self):
        changes = self.df['population'].pct_change().dropna() * 100
        max_idx = changes.idxmax()
        min_idx = changes.idxmin()
        return {
            'max_growth': round(changes[max_idx], 2),
            'max_growth_year': int(max_idx),
            'max_decline': round(changes[min_idx], 2),
            'max_decline_year': int(min_idx)
        }

    def moving_average_forecast(self, n_periods=3, forecast_years=5):
        data = self.df['population'].values
        forecasts = []
        last_years = data[-n_periods:].tolist()
        last_year = self.df['year'].iloc[-1]
        for i in range(forecast_years):
            next_val = sum(last_years[-n_periods:]) / n_periods
            forecasts.append(next_val)
            last_years.append(next_val)
        forecast_years_list = [last_year + i + 1 for i in range(forecast_years)]
        return forecast_years_list, forecasts

    def plot_forecast(self, ax, n_periods, forecast_years):
        forecast_years_list, forecasts = self.moving_average_forecast(n_periods, forecast_years)
        full_years = list(self.df['year']) + forecast_years_list
        full_values = list(self.df['population']) + forecasts
        ax.plot(full_years, full_values, 'o-', label='Исторические данные', color='blue')
        ax.plot(forecast_years_list, forecasts, 'o-', label='Прогноз', color='red')
        ax.axvline(x=self.df['year'].iloc[-1], color='gray', linestyle='--', alpha=0.7)
        ax.set_title('Прогноз численности населения (скользящая средняя)')
        ax.set_xlabel('Год')
        ax.set_ylabel('Численность')
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.6)
        return full_years, full_values
        # добавлена проверка данных
        fix: добавил комментарий
