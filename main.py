import sys
import math
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QVBoxLayout, QWidget, QStatusBar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
exp = 2.718

def f(x, y):
    return x * x - x + y
def F(x):
    return -x*x-x-1+math.pow(exp, x)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Создаем элементы управления
        self.input_coord = QLineEdit(self)
        self.input_x = QLineEdit(self)
        self.input_h = QLineEdit(self)
        self.button_plot = QPushButton('Метод Эйлера', self)
        self.button_plot1 = QPushButton('Метод Эйлера исправленный', self)
        self.button_plot2 = QPushButton('метод Рунге–Кутты–Мерсона', self)
        self.button_plot3 = QPushButton('метод Адамса 4-го порядка', self)
        self.button_plot4 = QPushButton('Аналитическое решение', self)
        self.button_plot5 = QPushButton('Очистить', self)
        self.figure_canvas = FigureCanvas(Figure(figsize=(100, 100)))
        self.status_bar = QStatusBar()
        self.fig = Figure()

        # Создаем холст с графиками
        self.ax1 = self.fig.add_subplot(111)

        # Устанавливаем заголовки графиков
        self.ax1.set_title('График')

        # Отображаем графики на холсте
        self.figure_canvas.figure = self.fig
        self.figure_canvas.draw()
        # Создаем разметку интерфейса
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.input_coord)
        layout.addWidget(self.input_x)
        layout.addWidget(self.input_h)
        layout.addWidget(self.button_plot)
        layout.addWidget(self.button_plot1)
        layout.addWidget(self.button_plot2)
        layout.addWidget(self.button_plot3)
        layout.addWidget(self.button_plot4)
        layout.addWidget(self.button_plot5)
        layout.addWidget(self.figure_canvas)

        # Настраиваем элементы управления
        self.input_coord.setPlaceholderText('Введите координаты начальной точки через запятую')
        self.input_x.setPlaceholderText('Введите абциссу конечной точки')
        self.input_h.setPlaceholderText('Введите шаг')
        self.button_plot.clicked.connect(self.plot)
        self.button_plot1.clicked.connect(self.plot1)
        self.button_plot2.clicked.connect(self.plot2)
        self.button_plot3.clicked.connect(self.plot3)
        self.button_plot4.clicked.connect(self.plot4)
        self.button_plot5.clicked.connect(self.plot5)
        # Настраиваем статус-бар
        self.setStatusBar(self.status_bar)

    def plot(self):
        # Получаем значения x и y и h
        coord_values = list(map(float, self.input_coord.text().split(',')))
        x_n = float(self.input_x.text())
        h = float(self.input_h.text())
        x = np.arange(coord_values[0], x_n + h, h)
        y = np.zeros_like(x)
        y[0] = coord_values[1]

        for i in range(len(x) - 1):
            y[i+1] = y[i] + h * f(x[i], y[i])

        # Создаем график
        self.ax1.plot(x, y)
        self.ax1.grid(True)
        # Отображаем графики на холсте
        self.figure_canvas.draw()

        # Обновляем статус-бар
        self.status_bar.showMessage('График построен')

    def plot1(self):

        # Получаем значения x и y и h
        coord_values = list(map(float, self.input_coord.text().split(',')))
        x_n = float(self.input_x.text())
        h = float(self.input_h.text())
        x = np.arange(coord_values[0], x_n + h, h)
        y = np.zeros_like(x)
        y[0] = coord_values[1]

        for i in range(len(x) - 1):
            y_euler = y[i] + h * f(x[i], y[i])
            y[i + 1] = y[i] + h / 2 * (f(x[i], y[i]) + f(x[i + 1], y_euler))
        # Создаем график
        self.ax1.plot(x, y)
        self.ax1.grid(True)
        # Отображаем графики на холсте
        self.figure_canvas.draw()
        # Обновляем статус-бар
        self.status_bar.showMessage('График построен')

    def plot2(self):

        # Получаем значения x и y и h
        coord_values = list(map(float, self.input_coord.text().split(',')))
        x_n = float(self.input_x.text())
        h = float(self.input_h.text())
        x = [coord_values[0]]
        y = [coord_values[1]]
        i=0
        atol =0.001
        while (x[i] < x_n):
            # Рассчитываем коэффициенты K1-K5
            k1 = h * f(x[i], y[i])
            k2 = h * f(x[i] + h / 3, y[i] + k1 / 3)
            k3 = h * f(x[i] + h / 3, y[i] + k1 / 6 + k2 / 6)
            k4 = h * f(x[i] + h / 2, y[i] + k1 / 8 + 3 / 8 * k3)
            k5 = h * f(x[i] + h, y[i] + k1 / 2 - 3 / 2 * k3 + 2 * k4)
            eps = abs((2 * k1 - 9 * k3 + 8 * k4 - k5) / h)

            if eps < atol / 32:
                h *= 2
            elif eps > atol:
                h /= 2
            else:
                x_new = x[i] + h
                y_new = y[i] + (k1 + 4 * k4 + k5) / 6
                i += 1
                x.append(x_new)
                y.append(y_new)

        # Создаем график
        self.ax1.plot(x, y)
        self.ax1.grid(True)
        # Отображаем графики на холсте
        self.figure_canvas.draw()
        # Обновляем статус-бар
        self.status_bar.showMessage('График построен')

    def plot3(self):

        # Получаем значения x и y и h
        coord_values = list(map(float, self.input_coord.text().split(',')))
        x_n = float(self.input_x.text())
        h = float(self.input_h.text())
        x = [coord_values[0]]
        y = [coord_values[1]]
        n = int((x_n-coord_values[0])/h)
        # Используем метод Рунге-Кутты 4 порядка для вычисления первых 4 значений
        for i in range(4):
            k1 = h * f(x[i], y[i])
            k2 = h * f(x[i] + h / 2, y[i] + k1 / 2)
            k3 = h * f(x[i] + h / 2, y[i] + k2 / 2)
            k4 = h * f(x[i] + h, y[i] + k3)

            y_next = y[i] + 1 / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
            y.append(y_next)

            x_next = x[i] + h
            x.append(x_next)
        for i in range(4, n):
            y_n = y[i]+h/24*(55*f(x[i],y[i])-59*f(x[i-1],y[i-1])+37*f(x[i-2],y[i-2])-9*f(x[i-3],y[i-3]))
            y.append(y_n)
            x_next = x[i] + h
            x.append(x_next)

        # Создаем график
        self.ax1.plot(x, y)
        self.ax1.grid(True)
        # Отображаем графики на холсте
        self.figure_canvas.draw()
        # Обновляем статус-бар
        self.status_bar.showMessage('График построен')
    def plot4(self):

        # Получаем значения x и y и h
        coord_values = list(map(float, self.input_coord.text().split(',')))
        x_n = float(self.input_x.text())
        h = float(self.input_h.text())
        n = int((x_n - coord_values[0]) / h)
        x = [coord_values[0]]
        y = [F(x[0])]
        for i in range(1,n+1):
            x_next = x[i-1]+h
            x.append(x_next)
            y_next = F(x[i])
            y.append(y_next)
        self.ax1.plot(x, y)
        self.ax1.grid(True)
        # Отображаем графики на холсте
        self.figure_canvas.draw()
        # Обновляем статус-бар
        self.status_bar.showMessage('График построен')
    def plot5(self):
        self.ax1.cla()
        self.figure_canvas.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

