import json
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

BASE_URL = "https://pokeapi.co/api/v2"


def get_json(path: str) -> dict:
    request = Request(BASE_URL + path, headers={"User-Agent": "python-practice/1.0"})
    with urlopen(request, timeout=10) as response:
        return json.load(response)


def main() -> None:
    try:
        names = [item["name"] for item in get_json("/pokemon?limit=20")["results"]]
        print("Первые 20 покемонов:")
        for index, name in enumerate(names, 1):
            print(f"{index:2}. {name}")
        name = input("Имя покемона: ").strip().lower()
        if not name:
            print("Имя не введено")
            return
        pokemon = get_json("/pokemon/" + quote(name, safe=""))
        print(f"Имя: {pokemon['name']}")
        print("Тип: " + ", ".join(item["type"]["name"] for item in pokemon["types"]))
        print(f"Вес: {pokemon['weight'] / 10:g} кг")
        print(f"Рост: {pokemon['height'] / 10:g} м")
        print("Способности: " + ", ".join(item["ability"]["name"] for item in pokemon["abilities"]))
    except HTTPError as error:
        print("Покемон не найден" if error.code == 404 else f"Ошибка API: {error.code}")
    except (URLError, TimeoutError, ValueError, KeyError) as error:
        print(f"Не удалось получить данные: {error}")


if __name__ == "__main__":
    main()
