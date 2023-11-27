import math

class GPS:
    def __init__(self, x=None, y=None, z=None):
        self.x = x
        self.y = y
        self.z = z

    def get_coord(self):
        return {"x": self.x, "y": self.y, "z": self.z}

    def distance_to(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2 + (self.z - other.z)**2)

class Dron:
    def __init__(self, start_gps, name):
        self.gps = start_gps
        self.name = name
        self.speed = 40
        self.angular_speed = 5  # Угловая скорость

    def move(self, kp, coord_dest, dt):
        distance = self.gps.distance_to(coord_dest)
        if distance < 1:
            print("Мы на месте")
            exit()
        else:
            u_x, u_y = self.calc(kp, coord_dest)
            self.gps.x += u_x * self.speed * dt
            self.gps.y += u_y * self.speed * dt

    def calc(self, kp, coord_dest):
        u_x = kp * (coord_dest.x - self.gps.x)
        u_y = kp * (coord_dest.y - self.gps.y)
        return u_x, u_y

    def time_fly(self, coord_dest):
        return self.gps.distance_to(coord_dest) / self.speed

# Пример использования
start_position = GPS(x=0, y=0, z=0)
destination = GPS(x=100, y=100, z=0)
drone = Dron(start_position, "MyDrone")

# Двигаться к координатам destination с временным шагом 0.1
for _ in range(100):
    drone.move(0.1, destination, 0.1)
    current_position = drone.gps.get_coord()
    print(f"Current Position: {current_position}")
