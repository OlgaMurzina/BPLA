"""Инструкция:

Шаг 1. Напишите функцию получения данных с датчика GPS. +

Шаг 2. Постройте визуализацию в виде графика изменения высоты полета. +

Шаг 3. Постройте траекторию маршрута, используя данные о координатах с датчика GPS.  +

Шаг 4. Рассчитайте длину траектории полета. +

Шаг 5. Опубликуйте результат выполнения задания в LMS Odin.   +"""

import math
import matplotlib.pyplot as plt
from random import uniform
import time
import folium


class GPS:
    """
    Класс получения координат с GPS
    """

    def __init__(self, x: float = None, y: float = None, z: float = None) -> None:
        """
        Конструктор класса GPS
        :param x: координата х
        :param y: координата у
        :param z: координата z
        """
        self.x = x
        self.y = y
        self.z = z
        self.dist = 0

    def get_coord(self) -> dict:
        """
        Метод возврат значений координат х, у и z дрона
        :return: словарь с координатами х, у и z
        """
        return {"x": self.x, "y": self.y, "z": self.z}

    def change_coordinates(self) -> None:
        """
        Метод изменения координат дрона при эмуляции полета. Меняет состояние глобальных переменных
        :return: Ничего
        """
        self.x += uniform(-0.1, 0.1)
        self.y += uniform(-0.1, 0.1)
        self.z += uniform(-0.1, 0.1)

    def distance_to(self, other) -> float:
        """
        Расчет дистанции по методу Евклида
        :param other: словарь с кооринатами точки назначения
        :return: величина расстояния от текущей точки до заданной
        """
        s = math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2)
        self.dist += s
        return s


def plot_dist(start, drone_data):
    """
    Метод отображает движение дрона на карте
    :return:
    """
    map = folium.Map(location=start[:-1],
                     zoom_start=11)
    trial_coordinates = [(drone_data['x'][i], drone_data['y'][i]) for i in range(len(drone_data))]
    folium.PolyLine(trial_coordinates, tooltip='Coast').add_to(map)
    # график тракетории дрона на карте в файле drone_trajectory.html
    map.save("drone_trajectory.html")


def plot_altitude(drone_data) -> None:
    """                         # display russia map

    Функция для построения графиrussia_map
    ка высоты дрона
    :param drone_data: словарь с данным, где в виде списков содержатся данные о времени и координатах полета дрона
    :return: график
    """
    plt.plot(drone_data['time'], drone_data['z'], label=drone_data['z'][::20])
    plt.xlabel('Время (с)')
    plt.ylabel('Высота (м)')
    plt.title('График высоты дрона в полете')
    plt.legend()
    plt.show(block=True)


def collect_data(end_time: time, gps: GPS) -> dict:
    """
    Функция сбора данных о полете в словарь
    :param end_time: время окончания полета
    :param gps: экземпляр класса с начальными данными
    :return: словарь с данными о полете
    """
    drone_data = {'time': [],
                  'x': [],
                  'y': [],
                  'z': [],
                  'dist': []}
    t = 0
    drone_data['time'].append(t)
    drone_data['x'].append(gps.x)
    drone_data['y'].append(gps.y)
    drone_data['z'].append(gps.z)
    drone_data['dist'].append(gps.dist)
    while t <= end_time:
        t += 1
        old_coord = gps.get_coord()
        other = GPS(x=old_coord.get('x'), y=old_coord.get('y'), z=old_coord.get('z'))
        gps.change_coordinates()
        drone_data['time'].append(t)
        drone_data['x'].append(gps.x)
        drone_data['y'].append(gps.y)
        drone_data['z'].append(round(gps.z, 2))
        gps.distance_to(other)
        drone_data['dist'].append(gps.dist)
    return drone_data


if __name__ == "__main__":
    # определяемм точку старта дрона
    start = [56.3264816, 44.0051395, 1.5]
    # создаем экземпляр класса GPS для работы с координатами дрона
    gps = GPS(x=start[0], y=start[1], z=start[2])
    # генерим эмуляцию полета дрона по времени
    drone_data = collect_data(end_time=150, gps=gps)
    # выводим длину траектории, которую пролетел дрон в условных единицах
    print(f'Длина траектории дрона: {drone_data["dist"][-1]}')
    # рисуем тракеторию дрона на карте с центром в точке старта
    plot_dist(start, drone_data)
    # выводим график изменения выстоты дрона по времени
    plot_altitude(drone_data)
