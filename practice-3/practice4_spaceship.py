from dataclasses import dataclass, field


@dataclass
class CrewMember:
    name: str
    role: str
    skills: set[str]
    health: int = 100

    def injure(self, amount: int) -> None:
        self.health = max(0, self.health - max(0, amount))

    def heal(self, amount: int) -> None:
        self.health = min(100, self.health + max(0, amount))


@dataclass
class SpaceShip:
    name: str
    fuel: int
    hull: int = 100
    speed: int = 0

    def accelerate(self, increment: int) -> None:
        if increment <= 0 or increment > self.fuel:
            raise ValueError("Для ускорения требуется положительное количество доступного топлива")
        self.fuel -= increment
        self.speed += increment

    def take_damage(self, amount: int) -> None:
        self.hull = max(0, self.hull - max(0, amount))
        if self.hull == 0:
            self.speed = 0

    def repair(self, amount: int) -> None:
        self.hull = min(100, self.hull + max(0, amount))


@dataclass
class Mission:
    objective: str
    ship: SpaceShip
    crew: list[CrewMember]
    resources: dict[str, int] = field(default_factory=lambda: {"запчасти": 0, "аптечки": 0})
    events: list[str] = field(default_factory=list)

    def asteroid(self, damage: int) -> None:
        self.ship.take_damage(damage)
        if self.crew:
            self.crew[0].injure(damage // 2)
        self.events.append(f"Столкновение с астероидом: урон {damage}")

    def repair_ship(self, engineer: CrewMember, amount: int) -> None:
        if engineer not in self.crew or engineer.role != "инженер" or "ремонт" not in engineer.skills:
            raise ValueError("Для ремонта нужен инженер с навыком ремонта")
        if self.resources.get("запчасти", 0) < 1:
            raise ValueError("Нет запчастей")
        self.resources["запчасти"] -= 1
        self.ship.repair(amount)
        self.events.append(f"{engineer.name} починил корпус на {amount}")

    def treat(self, patient: CrewMember, amount: int) -> None:
        if patient not in self.crew or self.resources.get("аптечки", 0) < 1:
            raise ValueError("Нет члена экипажа или аптечки")
        self.resources["аптечки"] -= 1
        patient.heal(amount)
        self.events.append(f"{patient.name}: здоровье восстановлено")


if __name__ == "__main__":
    pilot = CrewMember("Анна", "пилот", {"навигация"})
    engineer = CrewMember("Борис", "инженер", {"ремонт"})
    mission = Mission("Достичь орбиты Марса", SpaceShip("Заря", 30),
                      [pilot, engineer], {"запчасти": 2, "аптечки": 1})
    mission.ship.accelerate(10)
    mission.asteroid(25)
    mission.repair_ship(engineer, 20)
    mission.treat(pilot, 10)
    print(f"Цель: {mission.objective}")
    print(f"Топливо: {mission.ship.fuel}; корпус: {mission.ship.hull}; скорость: {mission.ship.speed}")
    print(f"Здоровье пилота: {pilot.health}; ресурсы: {mission.resources}")
    for event in mission.events:
        print(event)
