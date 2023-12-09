import random
import sys
import math
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QLineEdit, QGroupBox, QProgressBar
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QImage, QPixmap
import cv2


class DroneControlUI(QMainWindow):
    """
    Класс управледния дроном
    """

    def __init__(self):
        """
        Конструктор класса - начальная позиция, дистанция, экземпрял класса Дрон, инициализиация оконного интерфейса
        """
        super().__init__()
        self.start_position = GPS(x=0, y=0, z=0)
        self.destination = GPS(x=100, y=100, z=0)
        self.drone = Drone(start_position, "MyDrone")

        self.setWindowTitle("Управление дроном")
        self.setGeometry(100, 100, 300, 500)
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.lbl_video = QLabel(self)
        self.layout_video = QVBoxLayout()
        self.layout_video.addWidget(self.lbl_video)
        layout.addLayout(self.layout_video)

        self.video_capture = cv2.VideoCapture(0)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

        lbl_mode = QLabel("Выберите режим дрона:")
        # layout.addWidget(lbl_mode)

        cb_mode = QComboBox()
        cb_mode.addItems(["Автоматический", "Ручной", "Преследование",
                          "Cтабилизатор", "Разведка", "Демо",
                          "Свободный поиск", "Калибровка положения", "Спортивный",
                          "Нормальный", "Кино", "Самотестирования", "acro"])
        # layout.addWidget(cb_mode)
        layout_mode = QHBoxLayout()
        layout.addLayout(layout_mode)
        layout_mode.addWidget(lbl_mode)
        layout_mode.addWidget(cb_mode)

        btn_takeoff = QPushButton("Взлететь")
        btn_land = QPushButton("Приземлиться")
        layout_btn_fly = QHBoxLayout()
        layout_btn_fly.addWidget(btn_takeoff)
        layout_btn_fly.addWidget(btn_land)
        layout.addLayout(layout_btn_fly)

        gb_mission = QGroupBox("Ограничения миссии:")
        gb_mission.setMaximumHeight(75)
        hl_mission = QHBoxLayout()
        gb_mission.setLayout(hl_mission)

        vl_mission_1 = QVBoxLayout()
        vl_mission_2 = QVBoxLayout()
        vl_mission_3 = QVBoxLayout()

        lbl_altitude = QLabel("Высота")
        le_altitude = QLineEdit()
        vl_mission_1.addWidget(lbl_altitude)
        vl_mission_1.addWidget(le_altitude)
        hl_mission.addLayout(vl_mission_1)

        lbl_time = QLabel("Время")
        le_time = QLineEdit()
        vl_mission_2.addWidget(lbl_time)
        vl_mission_2.addWidget(le_time)
        hl_mission.addLayout(vl_mission_2)

        lbl_dist = QLabel("Расстояние")
        le_dist = QLineEdit()
        vl_mission_3.addWidget(lbl_dist)
        vl_mission_3.addWidget(le_dist)
        hl_mission.addLayout(vl_mission_3)

        layout.addWidget(gb_mission)

        gb_idicator = QGroupBox("Индикаторы:")
        gb_idicator.setMaximumHeight(100)
        hl_idicator = QHBoxLayout()
        gb_idicator.setLayout(hl_idicator)

        vl_idicator_1 = QVBoxLayout()
        vl_idicator_2 = QVBoxLayout()
        vl_idicator_3 = QVBoxLayout()

        self.battery_level = 100
        lbl_capasity = QLabel("Заряд")
        self.le_capasity = QLabel(f"{self.battery_level}%")

        self.timer_battery = QTimer(self)
        self.timer_battery.timeout.connect(self.get_battery_level)
        self.timer_battery.start(1000)

        self.battery_indicator = QProgressBar()
        self.battery_indicator.setMaximum(100)
        self.battery_indicator.setValue(100)

        vl_idicator_1.addWidget(lbl_capasity)
        vl_idicator_1.addWidget(self.battery_indicator)
        vl_idicator_1.addWidget(self.le_capasity)
        hl_idicator.addLayout(vl_idicator_1)

        lbl_direction = QLabel("\t   Направление\nКурс\t|       Тангаж\t|    Крен")
        lbl_direction_value = QLabel("  45\t|         -30\t|      20")
        vl_idicator_2.addWidget(lbl_direction)
        vl_idicator_2.addWidget(lbl_direction_value)
        hl_idicator.addLayout(vl_idicator_2)

        layout.addWidget(gb_idicator)

        self.lbl_gps = QLabel("GPS")
        self.lbl_coord = QLabel("x=0; y=0; z=0")
        self.btn_gps = QPushButton("↻")
        self.btn_gps.clicked.connect(self.update_gps)
        layout_gps = QHBoxLayout()
        layout_gps.addWidget(self.lbl_gps)
        layout_gps.addWidget(self.lbl_coord)
        layout_gps.addWidget(self.btn_gps)
        layout.addLayout(layout_gps)

    def get_battery_level(self) -> None:
        """
        Метод класса - учитывает заряд батареи
        """
        if self.battery_level > 0:
            self.battery_level -= 1
            self.le_capasity.setText(f"{self.battery_level}%")
            self.battery_indicator.setValue(self.battery_level)
            if self.battery_level < 10:
                self.battery_indicator.setStyleSheet("QProgressBar::chunk { background-color: red; }")

    def update_frame(self) -> None:
        """
        Метод класса - обновляет фреймы при распознавании видео
        """
        ret, frame = self.video_capture.read()
        if ret:
            height, width, channal = frame.shape
            bytes_per_line = 3 * width

            q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format.Format_BGR888)
            pixmap = QPixmap.fromImage(q_image)
            self.lbl_video.setPixmap(pixmap)

    def update_gps(self) -> None:
        """
        Метод класса - обновляет показания GPS-датчика
        """
        self.drone.move(0.1, destination, 0.1)
        current_position = drone.gps.get_coord()
        self.lbl_coord.setText(f'x:{current_position["x"]}, '
                               f'y:{current_position["y"]}, '
                               f'z:{current_position["z"]}, ')


class GPS:
    """
    Класс GPS-датчика
    """

    def __init__(self, x=None, y=None, z=None) -> None:
        """
        Конструктор класса
        :param x: координата х
        :param y: координата у
        :param z: координата  я
        """
        self.x = x
        self.y = y
        self.z = z

    def get_coord(self) -> dict:
        """
        Метод класса GPS - возрвщает текущие координаты объекта
        :return:
        """
        return {"x": self.x, "y": self.y, "z": self.z}

    def distance_to(self, other) -> float:
        """
        Метод класса - возвращает расстояние от текущей точки до заданной точки
        :param other: координаты заданной точки в формате dict
        :return: расстояние от текущей точки до заданной точки
        """
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2)


class Drone:
    """
    Класс Drone - дрона
    """

    def __init__(self, start_gps, name) -> None:
        """
        Конструктор класса дрона
        :param start_gps: начальные координаты дрона
        :param name: имя дрона
        """
        self.gps = start_gps
        self.name = name
        # скорость дрона
        self.speed = 40
        # угловая скорость дрона
        self.angular_speed = 5
        # начальный запас батареи
        self.capasity = 100
        # тангаж, крен и направление (курс)
        self.pitch, self.roll, self.yaw = 0, 0, 0
        # пределы высоты, времени и дистанции
        self.stop_altitude, self.stop_time, self.stop_dist = 500, 25, 5

    def move(self, kp, coord_dest, dt) -> None:
        """
        Метод управления полетом
        :param kp: коэффицент пропорциональности
        :param coord_dest: координаты места назначения в формате dict
        :param dt: временной интервал
        """
        distance = self.gps.distance_to(coord_dest)
        if distance < 1:
            print("Мы на месте")
        else:
            u_x, u_y = self.calc(kp, coord_dest)
            self.gps.x += u_x * self.speed * dt
            self.gps.y += u_y * self.speed * dt

    def calc(self, kp, coord_dest) -> tuple:
        """
        Метод расчета управляющего воздействия по кр
        :param kp: коэффициент пропорциональности
        :param coord_dest: координаты места назначения в формате dict
        :return: управляющее воздействие по х, управляющее воздейтсвие по у
        """
        u_x = kp * (coord_dest.x - self.gps.x)
        u_y = kp * (coord_dest.y - self.gps.y)
        return u_x, u_y


if __name__ == "__main__":
    # начальное положение дрона
    start_position = GPS(x=0, y=0, z=0)
    # конечный пункт назначения
    destination = GPS(x=100, y=100, z=0)
    # инициализация дрона
    drone = Drone(start_position, "MyDrone")
    # запуск оконного интерфейса для управления дроном
    app = QApplication([])
    window = DroneControlUI()
    window.show()
    sys.exit(app.exec())
