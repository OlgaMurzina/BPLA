# блок импорта
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import pandas as pd

# seed определяет набор для генерации случайных чисел в зависимости от числа, указанного в скобках
np.random.seed(42)

# генериуем даныне - время и скорость
# создадим линейную зависимость скорости от времени
time = np.sort(5 * np.random.rand(300, 1), axis=0)
speed = 3 * time + 2 + np.random.randn(300, 1)
# для повышения точности предсказания создаем синтетические признаки из квадрата и куба скоростей
df = pd.DataFrame(data=time, columns=['time'])
df['speed'] = speed
df['speed2'] = df['speed'].apply(lambda x: x ** 2)
df['speed3'] = df['speed'].apply(lambda x: x ** 3)

# разделим данные на обучающий и тестовый наборы
target = df['speed']
features = df.drop('speed', axis=1)
features_train, features_test, target_train, target_test = train_test_split(features, target,
                                                                             test_size=0.2, random_state=42)
# создаем модель и обучаем ее
model = LinearRegression()
model.fit(features_train, target_train)
# предсказываем скорость для тестовго набора данных
predict = model.predict(features_test)

# оценка качества модели
mse = mean_squared_error(target_test, predict)
print(f'mse = {mse}')

# визуализируем данные
plt.scatter(features_test['time'], target_test , color='blue', linewidth=6, label='Реальные данные')
plt.scatter(features_test['time'], predict, color='red', linewidth=3, label='Предсказанные данные')
plt.xlabel('Time')
plt.ylabel('Speed')
plt.legend()
plt.show()
