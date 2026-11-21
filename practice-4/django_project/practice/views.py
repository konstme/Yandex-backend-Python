from django.http import HttpResponseNotAllowed
from django.shortcuts import redirect, render
from django.urls import reverse
from urllib.parse import urlencode

from .api import APIError, dog_breeds, dog_image, pokemon


def home(request):
    return render(request, "home.html")


def dogs(request):
    context = {"breeds": [], "photos": [], "entered": ""}
    try:
        context["breeds"] = dog_breeds()
        if request.method == "POST":
            context["entered"] = request.POST.get("breeds", "")
            requested = list(dict.fromkeys(
                value.strip().lower() for value in context["entered"].split(",") if value.strip()
            ))
            known = set(context["breeds"])
            for breed in requested[:10]:
                if breed in known:
                    context["photos"].append({"breed": breed, "url": dog_image(breed)})
                else:
                    context.setdefault("errors", []).append(f"Неизвестная порода: {breed}")
            if len(requested) > 10:
                context.setdefault("errors", []).append("Показаны только первые 10 пород")
    except APIError as error:
        context.setdefault("errors", []).append(str(error))
    return render(request, "dogs.html", context)


def team(request):
    members = request.session.get("team", [])
    return render(request, "team.html", {
        "members": members,
        "message": request.GET.get("message", ""),
        "error": request.GET.get("error", ""),
    })


def team_redirect(key, text):
    return redirect(reverse("team") + "?" + urlencode({key: text}))


def add_pokemon(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    name = request.POST.get("name", "").strip().lower()
    if not name:
        return team_redirect("error", "Введите имя покемона")
    members = request.session.get("team", [])
    if any(member["name"] == name for member in members):
        return team_redirect("error", "Этот покемон уже в команде")
    try:
        chosen = pokemon(name)
    except APIError as error:
        return team_redirect("error", str(error))
    if any(member["name"] == chosen["name"] for member in members):
        return team_redirect("error", "Этот покемон уже в команде")
    request.session["team"] = members + [chosen]
    return team_redirect("message", f"{chosen['name']} добавлен в команду")


def remove_pokemon(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    name = request.POST.get("name", "")
    members = request.session.get("team", [])
    request.session["team"] = [member for member in members if member["name"] != name]
    return team_redirect("message", f"{name} удалён из команды")


def search_pokemon(request):
    name = request.GET.get("name", "").strip().lower()
    if not name:
        return render(request, "search.html", {"error": "Введите имя покемона"})
    try:
        found = pokemon(name)
        return render(request, "search.html", {"found": found, "query": name})
    except APIError as error:
        return render(request, "search.html", {"error": str(error), "query": name})


def simulate_battle(first, second):
    hp = [max(1, first["hp"]), max(1, second["hp"])]
    fighters = [first, second]
    turn = 0 if first["speed"] >= second["speed"] else 1
    log = []
    for _ in range(200):
        defender = 1 - turn
        damage = max(1, round(fighters[turn]["attack"] * 12 /
                              (fighters[defender]["defense"] + 12)))
        hp[defender] = max(0, hp[defender] - damage)
        log.append(f"{fighters[turn]['name']} наносит {damage} урона; "
                   f"у {fighters[defender]['name']} осталось {hp[defender]} HP")
        if hp[defender] == 0:
            return fighters[turn]["name"], log
        turn = defender
    return "Ничья", log


def battle(request):
    members = request.session.get("team", [])
    if request.method == "POST":
        first_name = request.POST.get("first")
        second_name = request.POST.get("second")
        chosen = {member["name"]: member for member in members}
        if first_name == second_name or first_name not in chosen or second_name not in chosen:
            return render(request, "battle.html", {"members": members,
                          "error": "Выберите двух разных покемонов из команды"})
        winner, log = simulate_battle(chosen[first_name], chosen[second_name])
        return render(request, "battle.html", {"members": members, "winner": winner,
                      "log": log, "first": first_name, "second": second_name})
    return render(request, "battle.html", {"members": members})
