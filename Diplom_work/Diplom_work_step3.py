# блок импорта
import math
import heapq
import matplotlib.pyplot as plt

class Node:
    """
    Класс узлов - вершин графов (2D)
    """
    def __init__(self, position, cost=0, heuristic=0, parent=None) -> None:
        """
        Конструктор класса узлов
        :param position: (x, y)
        :param cost: цена (время прохождения)
        :param heuristic: эвристика - (цена расстояния (времени) от текущего узла до желаемого)
        :param parent: узел-родитель
        """
        self.position = position
        self.cost = cost
        self.heuristic = heuristic
        self.parent = parent

    def total_cost(self) -> float:
        """
        Подсчет общей стоимости узла
        :return: общую стоимость
        """
        return self.heuristic + self.cost

    def __lt__(self, other: object) -> bool:
        """
        Метод очереди с приоритетами - какой узел эффективнее посетить
        :param other: узел для сравнения
        :return: bool
        """
        return self.total_cost() < other.total_cost()


class AStar:
    """
    Класс А-звезда - самый распространенный метод оптимизации пути
    """
    def __init__(self, grid: list) -> None:
        """
        Конструктор класса А-звезда
        :param grid: сетка из узлов
        """
        self.grid = grid
        # открытые узлы - в список
        self.open_set = []
        # закрытые узлы - множество
        self.closed_set = set()

    def heuristic(self, current: object, goal: object) -> float:
        """
        Метод для вычисления евклидова расстояния от текущего узла до цели
        :param current: текущий узел
        :param goal: цель
        :return: расстояние между текущим узлом и целью
        """
        return math.sqrt((current[0] - goal[0]) ** 2 + (current[1] - goal[1]) ** 2)

    def get_neighbors(self, node: object) -> list:
        """
        Метод вычисления положения ближайших соседей
        :param node: текущий узел
        :return: список кортежей координат ближайших соседей
        """
        x, y = node.position
        # все соседи справа, слева, сверху, снизу
        neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        return [(i, j) for i, j in neighbors if
                0 <= i < len(self.grid) and 0 <= j < len(self.grid[0]) and not self.grid[i][j]]

    def reconstruct_path(self, node: object) -> list:
        """
        Восстановление пути от конечного узла к начальному
        :param node: конечный узел
        :return: путь развернутый от начала к концу
        """
        path = []
        while node:
            path.append(node.position)
            node = node.parent
        return path[::-1]

    def find_path(self, start: object, goal: object) -> list or None:
        """
        Метод поиска пути
        :param start: координаты стартового узла х и у
        :param goal: координаты целевого узла х и у
        :return:
        """
        # стартовый узел
        start_node = Node(start)
        # эвристика между нашим стартовым и конечным узлом
        start_node.heuristic = self.heuristic(start, goal)
        # очередь с приоритетами - добавляем стартовый узел и опенсет, который хранит соседей стартового узла
        heapq.heappush(self.open_set, start_node)
        while self.open_set:
            # вынимаем узел с наименьшей стоимостью
            current_node = heapq.heappop(self.open_set)
            if current_node.position == goal:
                # если достигли цели, то возвращаем путь
                return self.reconstruct_path(current_node)
            # добавляем в множество просмотернных текущий узел
            self.closed_set.add(current_node.position)
            # проверяем всех соседей текущего узла
            for neighbor_pos in self.get_neighbors(current_node):
                # если сосед проверен, то мы его не смотрим
                if neighbor_pos in self.closed_set:
                    continue
                # создали соседа - как экземпляр класса узел
                neighbor_node = Node(neighbor_pos)
                # увеличиваем стоимость соседа на 1 по отношению к текущему - в итоге работает счетчик шагов
                neighbor_node.cost = current_node.cost + 1
                # рассчитываем эвристику от соседа до цели
                neighbor_node.heuristic = self.heuristic(neighbor_pos, goal)
                # помещаем в родители соседа текущий узел
                neighbor_node.parent = current_node
                # если наш сосед не в тех, которые не проверены, то ставим его в очередь на проверку
                if neighbor_node not in self.open_set:
                    heapq.heappush(self.open_set, neighbor_node)

        return None

def plot_path(grid, path) -> None:
    """
    Функция для построения графика пути с обходом препятствий
    :param grid: матрица, где обозначены препятствия
    :param path: найденный путь в обход препятствий
    :return: график
    """
    matr = [(x, y) for x in range(len(grid)) for y in range(len(grid[0]))]
    fig, ax = plt.subplots()
    fig.size=(20,10)
    for x, y in matr:
        if grid[x][y] == 1:
            ax.scatter(x, y, c='red', linewidth=10)
        else:
            ax.scatter(x, y, c='green', linewidth=10)
    for x, y in path:
        ax.scatter(x, y, c='blue', linewidth=3)
    ax.set_xlabel('columns')
    ax.set_ylabel('strings')
    ax.set_title('Path')

    ax.grid(True)
    plt.show(block=True)


grid = [
    [0, 0, 0, 1, 0, 0, 1, 0],
    [0, 1, 1, 1, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 1, 0, 1, 0, 0, 0],
    [1, 0, 0, 0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0, 0, 0, 0]
]

start_point = (0, 0)
goal_point = (7, 7)

astar = AStar(grid)
path = astar.find_path(start_point, goal_point)

if path:
    print("Оптимальный путь:", path)
    plot_path(grid, path)
else:
    print("Путь не найден.")



