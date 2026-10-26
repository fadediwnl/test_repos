import json
from collections import defaultdict


def group_users_by_city(users):
    """Возвращает словарь {город: [имена пользователей]}."""
    cities = defaultdict(list)
    for user in users:
        city = user.get("address", {}).get("city")
        if city is None:
            continue
        cities[city].append(user["name"])
    return dict(cities)


def main():
    with open("users.json", "r", encoding="utf-8") as f:
        users = json.load(f)

    cities = group_users_by_city(users)

    with open("cities.json", "w", encoding="utf-8") as f:
        json.dump(cities, f, ensure_ascii=False, indent=2)

    print(f"Сохранено городов: {len(cities)} -> cities.json")


if __name__ == "__main__":
    main()
