import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import pandas as pd
from variant5 import PopulationAnalysis
from variant10 import InflationAnalysis

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Лабораторная работа №3 — Статистика и прогнозирование")
        self.root.geometry("1300x800")

        self.current_variant = None
        self.analysis = None

        self.create_widgets()

    def create_widgets(self):
        # Левая панель
        left_frame = tk.Frame(self.root, width=350, bg='#f0f0f0', relief='sunken', borderwidth=2)
        left_frame.pack(side='left', fill='y', padx=5, pady=5)

        tk.Label(left_frame, text="Выберите вариант", font=('Arial', 14, 'bold'), bg='#f0f0f0').pack(pady=10)
        tk.Button(left_frame, text="Вариант 5 — Численность населения", command=self.load_variant5, width=30).pack(pady=5)
        tk.Button(left_frame, text="Вариант 10 — Инфляция", command=self.load_variant10, width=30).pack(pady=5)

        tk.Label(left_frame, text="Прогнозирование", font=('Arial', 12, 'bold'), bg='#f0f0f0').pack(pady=10)
        tk.Label(left_frame, text="Период скользящей средней (N):", bg='#f0f0f0').pack()
        self.n_spinbox = tk.Spinbox(left_frame, from_=2, to=10, width=10)
        self.n_spinbox.pack(pady=5)

        tk.Label(left_frame, text="Лет для прогноза:", bg='#f0f0f0').pack()
        self.forecast_spinbox = tk.Spinbox(left_frame, from_=1, to=10, width=10)
        self.forecast_spinbox.pack(pady=5)

        tk.Button(left_frame, text="Показать прогноз", command=self.show_forecast, width=30).pack(pady=10)
        tk.Button(left_frame, text="Экспорт графика", command=self.export_plot, width=30).pack(pady=5)

        # Правая часть (таблица + график)
        right_frame = tk.Frame(self.root)
        right_frame.pack(side='right', fill='both', expand=True, padx=5, pady=5)

        tk.Label(right_frame, text="Таблица данных", font=('Arial', 12, 'bold')).pack()
        self.table_frame = tk.Frame(right_frame)
        self.table_frame.pack(fill='both', expand=True, pady=5)

        tk.Label(right_frame, text="График", font=('Arial', 12, 'bold')).pack()
        self.figure = plt.Figure(figsize=(6, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=right_frame)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)

        # Панель инструментов для графика (масштабирование)
        toolbar_frame = tk.Frame(right_frame)
        toolbar_frame.pack(fill='x')
        self.toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame)
        self.toolbar.update()
    # загрузка данных для варианта 5
    def load_variant5(self):
        filepath = "data/population.csv"
        try:
            self.analysis = PopulationAnalysis(filepath)
            self.current_variant = 5
            self.display_table()
            self.plot_main_graph()
            messagebox.showinfo("Успех", "Вариант 5 загружен")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {e}")

    def load_variant10(self):
        filepath = "data/inflation.csv"
        try:
            self.analysis = InflationAnalysis(filepath)
            self.current_variant = 10
            self.display_table()
            self.plot_main_graph()
            messagebox.showinfo("Успех", "Вариант 10 загружен")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {e}")

    def display_table(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        data, columns = self.analysis.get_table_data()
        tree = ttk.Treeview(self.table_frame, columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        for row in data:
            tree.insert('', 'end', values=row)
        tree.pack(fill='both', expand=True)
        self.table = tree

    def plot_main_graph(self):
        self.ax.clear()
        self.analysis.plot_data(self.ax)
        self.canvas.draw()

    def show_forecast(self):
        if self.analysis is None:
            messagebox.showwarning("Ошибка", "Сначала выберите вариант")
            return

        n = int(self.n_spinbox.get())
        forecast_years = int(self.forecast_spinbox.get())

        self.ax.clear()
        self.analysis.plot_forecast(self.ax, n, forecast_years)
        self.canvas.draw()

    def export_plot(self):
        if self.analysis is None:
            messagebox.showwarning("Ошибка", "Сначала выберите вариант")
            return
        filepath = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if filepath:
            self.figure.savefig(filepath)
            messagebox.showinfo("Экспорт", f"График сохранён: {filepath}")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
    #добавил комментарий в функцию load_variant5
    docs: пояснил загрузку варианта 5
