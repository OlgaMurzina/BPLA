# блок импорта
from dronekit import connect, VehicleMode


def connect_to_vehicle(connection_string: str) -> object:
    """
    Функция для подключения к беспилотнику (БПЛА)
    :param connection_string: строка для подключения к беспилотнику
    :return: объект беспилотника, к которому подключились
    """
    # выводим информацию о начале процесса подключения
    print(f'Подключение к беспилотнику по адресу: {connection_string}')

    # устанавливаем соединение с БПЛА и ожидаем готовности
    vehicle = connect(connection_string, wait_ready=True)

    # выводим сообщение об успешном подключении
    print('Подключено к БПЛА')

    # возвращаем объект беспилотника
    return vehicle


def takeoff(vehicle: object, target_altitude: float):
    """
    Функция для выполнения взлета
    :param vehicle: объект беспилотника
    :param target_altitude:
    :return:
    """
    # выводим информацию о начале взлета
    print(f'Взлет на высоту {target_altitude} метров')

    # устанавливаем режим GUIDED и вооружаем БПЛА
    vehicle.mode = VehicleMode('GUIDED')
    vehicle.armed = True

    # инициируем взлет на указанную высоту
    vehicle.simple_takeoff(target_altitude)

    # ожидаем достижения заданной высоты
    while True:
        # выводим текущую высоту
        print('Высота: ', vehicle.location.global_relative_frame.alt)

        # проверяем, достигла ли высота 95% от целевой
        if vehicle.location.global_relative_frame.alt >= target_altitude * 0.95:
            # выводим сообщение о достижении высоты
            print('Высота достигнута!!')
            # выходим из цикла
            break


def main() -> None:
    """
    Главная функция управления БПЛА
    :return: None
    """
    # задаем адрес порта для соединения с БПЛА
    connection_string = '127.0.0.1:14550'

    # подключаемся к БПЛА
    vehicle = connect_to_vehicle(connection_string)

    # обработка исключения
    try:
        # вызываем функцию взлета с целевой высотой 10 метров
        takeoff(vehicle, target_altitude=10)

    finally:
        # завершаем программу и закрываем соединение с БПЛА
        vehicle.close()
        print('Соединение с БПЛА завершено')


if __name__ == '__main__':
    main()
