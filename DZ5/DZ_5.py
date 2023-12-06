"""
Шаг 1. Создайте новый проект в вашей среде разработки, назовите его «Детектор объектов». +

Шаг 2. Загрузите изображение с объектом, который вы хотите обнаружить, например, изображение машины.

Шаг 3. Используя библиотеку OpenCV для Python, напишите код, который будет обнаруживать машину на изображении. Воспользуйтесь, например, алгоритмом каскадных классификаторов Хаара (Haar Cascade).

Шаг 4. Добавьте код для вывода прямоугольной рамки вокруг найденного объекта (машины).

Шаг 5. Попробуйте запустить ваш код на других изображениях с машинами и проверьте, работает ли ваш детектор объектов правильно.

Шаг 6. Опубликуйте результат выполнения задания в LMS Odin.
"""

import cv2

# Загрузка предварительно обученного классификатора для обнаружения лиц
# human_cascade_face = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
human_cascade_smile = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
cars_cascade = cv2.CascadeClassifier('cars.xml')

# Открываем видеопоток
cap = cv2.VideoCapture("Cars2.mp4")  # Замените 'your_video.mp4' на имя вашего видеофайла

rectangle_face = None
def find_face(human_cascade):
    # Чтение кадра из видео
    ret, frame = cap.read()

    if not ret:
        return False

    # Преобразование кадра в оттенки серого
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Обнаружение человека на кадре
    humans = human_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    # Рисование прямоугольников вокруг обнаруженных людей
    for (x, y, w, h) in humans:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Отображение кадра
    cv2.imshow('Human Detection', frame)
    if len(humans) > 0:
        return humans[0]

def find_smile(human_cascade):
    # Чтение кадра из видео
    ret, frame = cap.read()

    if not ret:
        return False

    # Преобразование кадра в оттенки серого
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Обнаружение человека на кадре
    humans = human_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    # Рисование прямоугольников вокруг обнаруженных людей

    for (x, y, w, h) in humans:
        rectangle_face = (x, y, w, h)
        if rectangle_face is not None:
            x0, y0, w0, h0 = rectangle_face
            if x0 <= x <= x0 + w0 and y0 <= y <= y0 + h0 and w <= w0 and h <= h0:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Отображение кадра
    cv2.imshow('Human Detection', frame)



is_find = True
while is_find:

    rectangle_cars = find_face(cars_cascade)
    # find_smile(human_cascade_face)
    # Выход при нажатии клавиши 'q'
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

# Освобождение ресурсов и закрытие окон при завершении
cap.release()
cv2.destroyAllWindows()