import json
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen


class APIError(Exception):
    pass


def get_json(url: str) -> dict:
    try:
        with urlopen(Request(url, headers={"User-Agent": "python-practice/1.0"}), timeout=10) as response:
            return json.load(response)
    except HTTPError as error:
        if error.code == 404:
            raise APIError("Запись не найдена") from error
        raise APIError(f"Сервис ответил ошибкой {error.code}") from error
    except (URLError, TimeoutError, ValueError) as error:
        raise APIError("Сервис временно недоступен") from error


def dog_breeds() -> list[str]:
    data = get_json("https://dog.ceo/api/breeds/list/all")
    breeds = []
    for breed, subbreeds in data["message"].items():
        breeds.append(breed)
        breeds.extend(f"{subbreed} {breed}" for subbreed in subbreeds)
    return sorted(breeds)


def dog_image(breed: str) -> str:
    parts = breed.lower().split()
    path = "/".join(reversed(parts)) if len(parts) == 2 else parts[0]
    data = get_json(f"https://dog.ceo/api/breed/{quote(path, safe='/')}/images/random")
    return data["message"]


def pokemon(name: str) -> dict:
    data = get_json("https://pokeapi.co/api/v2/pokemon/" + quote(name.lower(), safe=""))
    stats = {item["stat"]["name"]: item["base_stat"] for item in data["stats"]}
    return {
        "name": data["name"],
        "types": [item["type"]["name"] for item in data["types"]],
        "abilities": [item["ability"]["name"] for item in data["abilities"]],
        "height": data["height"] / 10,
        "weight": data["weight"] / 10,
        "image": data.get("sprites", {}).get("front_default"),
        "hp": stats.get("hp", 1),
        "attack": stats.get("attack", 1),
        "defense": stats.get("defense", 1),
        "speed": stats.get("speed", 1),
    }
