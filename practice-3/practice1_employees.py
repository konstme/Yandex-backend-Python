from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Employee:
    name: str
    base_salary: Decimal

    def calculate_salary(self) -> Decimal:
        return self.base_salary


@dataclass
class Manager(Employee):
    team_size: int
    bonus_per_person: Decimal

    def calculate_salary(self) -> Decimal:
        return self.base_salary + self.team_size * self.bonus_per_person


@dataclass
class Developer(Employee):
    completed_tasks: int
    bonus_per_task: Decimal

    def calculate_salary(self) -> Decimal:
        return self.base_salary + self.completed_tasks * self.bonus_per_task


if __name__ == "__main__":
    staff = [
        Employee("Анна", Decimal("50000")),
        Manager("Борис", Decimal("80000"), 5, Decimal("3000")),
        Developer("Вера", Decimal("70000"), 8, Decimal("1500")),
    ]
    for person in staff:
        print(f"{person.name}: {person.calculate_salary():.2f} ₽")
