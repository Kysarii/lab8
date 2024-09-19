import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Класс Tariff, представляющий телефонный тариф
class Tariff:
    def __init__(self, tariff_name, customer, service_type):
        self.tariff_name = tariff_name  # Название тарифа
        self.customer = customer  # Заказчик
        self.service_type = service_type  # Тип услуги


# Класс для обработки тарифов
class TariffManager:
    def __init__(self):
        self.tariffs = []  # Список для хранения всех тарифов
        self.load_data()
        self.create_gui()

    # Метод загрузки данных из файла
    def load_data(self):
        try:
            with open("tariffs.txt", "r", encoding='cp1251') as file:
                for line in file:
                    tariff_name, customer, service_type = line.strip().split(",")
                    self.tariffs.append(Tariff(tariff_name, customer, service_type))
        except FileNotFoundError:
            print("Неверный формат данных")

    # Сегментация тарифов по заказчикам
    def segment_by_customer(self):
        customer_count = {}
        for tariff in self.tariffs:
            if tariff.customer in customer_count:
                customer_count[tariff.customer] += 1
            else:
                customer_count[tariff.customer] = 1
        return customer_count

    # Сегментация тарифов по видам услуг
    def segment_by_service_type(self):
        service_count = {}
        for tariff in self.tariffs:
            if tariff.service_type in service_count:
                service_count[tariff.service_type] += 1
            else:
                service_count[tariff.service_type] = 1
        return service_count

    def create_gui(self):
        self.root = tk.Tk()
        self.root.title("Тарифы")

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        window_width = 500
        window_height = 100
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Рамка для кнопок и отображения данных
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(pady=10)

        # Кнопки

        self.segment_by_customer_button = ttk.Button(self.main_frame, text="Сегментация по заказчикам", command=self.show_customer_data)
        self.segment_by_customer_button.pack(side=tk.LEFT, padx=10, pady = 20)

        self.segment_by_service_button = ttk.Button(self.main_frame, text="Сегментация по типам услуг", command=self.show_service_data)
        self.segment_by_service_button.pack(side=tk.LEFT, padx=10, pady = 20)

        # Рамка для диаграммы
        self.chart_frame = tk.Frame(self.root)
        self.chart_frame.pack(pady=10)
        self.root.mainloop()
    def visualize_data(self, data, title):
        labels = list(data.keys())
        sizes = list(data.values())
        fig, ax = plt.subplots(figsize=(15, 15))
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90,
               colors=['#66c2a5', '#fc8d62', '#8da0cb', '#e78ac3', '#a6d854', '#ffbb78', '#98df8a', '#c5b0d5',
                       '#ff69b4',
                       '#fffacd'])
        ax.axis('equal')
        ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
        plt.legend(title="Заказчики / Услуги", bbox_to_anchor=(1.05, 1), loc='upper right')
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        for widget in self.chart_frame.winfo_children():
            if widget != canvas.get_tk_widget():
                widget.destroy()

        new_width = 1500
        new_height = 800
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        new_x = (screen_width - new_width) // 2
        new_y = (screen_height - new_height) // 2
        self.root.geometry(f"{new_width}x{new_height}+{new_x}+{new_y}")

    def show_customer_data(self):
        customer_count = self.segment_by_customer()
        self.visualize_data(customer_count, "Распределение по заказчикам")

    def show_service_data(self):
        service_count = self.segment_by_service_type()
        self.visualize_data(service_count, "Распределение по услугам")

# Запуск приложения
if __name__ == "__main__":
    tariff = TariffManager()