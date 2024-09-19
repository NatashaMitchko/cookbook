from bs4 import BeautifulSoup
import requests

fractions = {
    "1/2": "½",
    "1/3": "⅓",
    "2/3": "⅔",
    "1/4": "¼",
    "3/4": "¾",
    "1/8": "⅛",
}

measures = {
    "tbsp": "tablespoon",
    "Tbsp": "tablespoon",
    "Tsp": "tablespoon",
    "tsp": "teaspoon",
}


def format(s: str) -> str:
    for k, v in fractions.items():
        s = s.replace(k, v)
    for k, v in measures.items():
        s = s.replace(k, v)
    return s


if __name__ == "__main__":
    import sys
    import json

    URL = "https://natashamitchko.com/cookbook"
    page = requests.get(URL)

    main_soup = BeautifulSoup(page.content, features="html.parser")

    BASE = "https://natashamitchko.com/"
    
    RECIPIES = []

    for link in main_soup.find_all("a"):
        path = link.get("href").rstrip(".html")
        url = BASE + path
        page = requests.get(url)
        soup = BeautifulSoup(page.content, features="html.parser")

        buttons = soup.find_all("button")
        if buttons:
            print(f"Versioned recipe, skipping {path}")
            continue

        title = soup.find("h1").text.strip()

        ingredients = []
        for i in soup.find_all("li"):
            formatted = format(i.text.strip())
            ingredients.append(formatted)

        steps = []
        for s in soup.find_all("p"):
            steps.append(s.text.strip())

        _, tag, slug = path.split("/")

        recipe = {
            "title": title,
            "slug": slug,
            "description": "",
            "ingredients": ingredients,
            "steps": steps,
            "tags": [],
            "status": "PUBLISHED",
        }

        RECIPIES.append(recipe)

    filename = sys.argv[1]
    with open(filename, "w") as f:
        for recipe in RECIPIES:
            f.write(json.dumps(recipe) + "\n")
