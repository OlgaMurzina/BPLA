# блок импорта
import cv2

# загрузка предварительно обученного классификатора для обнаружения машин и лиц
human_cascade_smile = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
cars_cascade = cv2.CascadeClassifier('cars.xml')

# открываем видеопоток
cap = cv2.VideoCapture("Cars2.mp4")

rectangle_face = None
def find_car(car_cascade):
    # чтение кадра из видео
    ret, frame = cap.read()

    if not ret:
        return False

    # преобразование кадра в оттенки серого
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # обнаружение человека на кадре
    cars = car_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    # рисование прямоугольников вокруг обнаруженных людей
    for (x, y, w, h) in cars:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # отображение кадра
    cv2.imshow('Cars Detection', frame)
    if len(cars) > 0:
        return cars[0]

def find_face(human_cascade):
    # чтение кадра из видео
    ret, frame = cap.read()

    if not ret:
        return False

    # преобразование кадра в оттенки серого
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # обнаружение человека на кадре
    humans = human_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    # рисование прямоугольников вокруг обнаруженных людей
    for (x, y, w, h) in humans:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # отображение кадра
    cv2.imshow('Human Detection', frame)



is_find = True
while is_find:
    # отображение машины в кадре
    rectangle_cars = find_face(cars_cascade)
    # выход при нажатии клавиши 'q'
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

# освобождение ресурсов и закрытие окон при завершении
cap.release()
cv2.destroyAllWindows()