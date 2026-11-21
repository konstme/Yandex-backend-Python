from dataclasses import dataclass


@dataclass
class Vehicle:
    brand: str

    def description(self) -> str:
        return f"Транспорт марки {self.brand}"


@dataclass
class Car(Vehicle):
    seats: int

    def description(self) -> str:
        return f"Автомобиль {self.brand}: {self.seats} мест"


@dataclass
class Bicycle(Vehicle):
    gears: int

    def description(self) -> str:
        return f"Велосипед {self.brand}: {self.gears} передач"


@dataclass
class Boat(Vehicle):
    capacity: int

    def description(self) -> str:
        return f"Лодка {self.brand}: вместимость {self.capacity} человек"


if __name__ == "__main__":
    vehicles: list[Vehicle] = [Car("Toyota", 5), Bicycle("Trek", 21), Boat("Yamaha", 6)]
    for vehicle in vehicles:
        print(vehicle.description())
