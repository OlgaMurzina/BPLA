# ПИД-регулятор с медианным фильтром

# блок импорта
import math
import statistics
from random import uniform


class Gyroscope:
    """
    Класс объекта Гироскоп. Возвращает случайные значения угловых скоростей в формате
    { "vx": 10.5,  Угловая скорость по оси X
      "vy": -3.2,  Угловая скорость по оси Y
      "vz": 7.8    Угловая скорость по оси Z  }
    """

    def __init__(self) -> None:
        """
        Конструктор класса, генерирует случайные вещественные значения в [-3.0, 3.0] для эмуляции угловой скорости в радиан/с
        """
        self.gyro = {'vx': 0.0,
                     'vy': 0.0,
                     'vz': 0.0}


    def generate_rates() -> None:
        """
        Генератор случайных значений угловых скоростей vx, vy, vz
        """
        self.gyro = {'vx': uniform(-3.0, 3.0),
                     'vy': uniform(-3.0, 3.0),
                     'vz': uniform(-3.0, 3.0)}

    def get_gyroscope(self) -> dict:
        """
        Возврат текущих значений гироскопа
        :return gyro: словарь со значениями угловых скоростей в проекциях х, у и z
        """
        return self.gyro


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

    def get_coord(self) -> dict:
        """
        Возврат значений координат х, у и z
        :return: словарь с координатами х, у и z
        """
        return {"x": self.x, "y": self.y, "z": self.z}

    def distance_to(self, other: dict) -> float:
        """
        Расчет дистанции по методу Евклида
        :param other: словарь с кооринатами точки назначения
        :return: величина расстояния от текущей точки до заданной
        """
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2)


class PIDController:
    """
    Класс PID-контроллера.
    """

    def __init__(self, kp: float, ki: float, kd: float) -> None:
        """
        Конструктор класса. Принимает и устанавливает коэффициенты:
        :param kp: пропрорциональный коэффициент
        :param ki: интегральный коэффициент
        :param kd: дифференциальный коэффициент
        prev_error - ошибка с предыдущего шага
        integral - значение интеграла???
        """
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.prev_error = 0
        self.integral = 0

    def calculate(self, error: float, dt: float) -> float:
        """
        Функция вычисления управляющего воздействия U
        :param error: текущая ошибка
        :param dt: временной шаг
        :return output: величина управляющего воздействия
        """
        self.integral += error * dt
        derivative = (error - self.prev_error) / dt
        output = self.kp * error + self.ki * self.integral + self.kd * derivative
        self.prev_error = error
        return output


def median_filter(data: list) -> float:
    """
    Простая реализация медианного фильтра для сглаживания управляющих сигналов PID
    :param data: управляющие сигналы PID
    :return : медианное значение от data
    """
    return statistics.median(data)


class Dron:
    """
    Класс Дрон
    """

    def __init__(self, start_gps: dict, name: str) -> None:
        """
        Конструктор класса Дрон.
        :param start_gps: начальные координаты GPS
        :param name: название дрона
        speed: скрость моторов в %
        angular_speed: угловая скорость в %
        pid_controller_x: управляющее воздействие по х
        pid_controller_y: управляющее воздействие по у
        gyroscope: проекции угловой скорости на оси х, у и z
        """
        self.gps = start_gps
        self.name = name
        self.speed = 40
        self.angular_speed = 5
        self.pid_controller_x = PIDController(kp=0.1, ki=0.01, kd=0.01)
        self.pid_controller_y = PIDController(kp=0.1, ki=0.01, kd=0.01)
        self.gyroscope = Gyroscope()

    def move(self, coord_dest: dict, dt: float) -> None:
        """
        Функция управления движением дрона:
        :param coord_dest: координаты пункта назначения
        :param dt: временной шаг
        :return: None
        """

        # получение значений с гироскопа
        self.gyroscope.generate_rates()
        v = self.gyroscope.get_gyroscope()
        vx, vy, vz = v['vx'], v['vy'], v['vz']
        print(f'Gyroscope: {v}')

        error_x = coord_dest.x - self.gps.x
        error_y = coord_dest.y - self.gps.y

        u_x = self.pid_controller_x.calculate(error_x, dt)
        u_y = self.pid_controller_y.calculate(error_y, dt)

        # Сглаживание управляющих сигналов с использованием медианного фильтра
        filtered_u_x = median_filter([u_x])
        filtered_u_y = median_filter([u_y])

        self.gps.x += filtered_u_x * self.speed * dt
        self.gps.y += filtered_u_y * self.speed * dt


# Пример использования
start_position = GPS(x=0, y=0, z=0)
destination = GPS(x=100, y=100, z=0)
drone = Dron(start_position, "MyDrone")

# Двигаться к координатам destination с временным шагом 0.1
for _ in range(100):
    drone.move(destination, 0.1)
    current_position = drone.gps.get_coord()
    print(f"Current Position: {current_position}")
