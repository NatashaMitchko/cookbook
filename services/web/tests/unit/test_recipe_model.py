from app.model.recipe import Recipe, PublishStatus, is_valid_slug, get_recipe_object


def test_recipe_initialization():
    title = "new recipe"
    recipe = Recipe(
        title,
        "i-am-a-slug",
        "",
        ["1 carrot", "2 peas"],
        ["cook 'em"],
        ["dinner"],
        PublishStatus.PENDING,
    )
    assert recipe.title == "New Recipe"
    assert recipe.title == title.title()
    assert type(recipe.status) == PublishStatus
    assert isinstance(recipe.tags, set)


def test_is_valid_slug():
    t = [
        ("is-a-valid-slug", True),
        ("valid", True),
        ("is-valid", True),
        (" untrimmed-whitespace ", False),
        ("no dash", False),
        ("dash-postfix-", False),
        ("-dash-prepend", False),
        ("too---many--dashes-between", False),
    ]

    for slug, expected in t:
        assert is_valid_slug(slug) == expected


def test_get_recipe_object():
    recipe_dict = {
        "title": "",
        "slug": "",
        "description": "",
        "ingredients": [],
        "steps": [],
        "tags": [],
        "status": "PENDING",
    }
    recipe_obj = get_recipe_object(recipe_dict)
    assert recipe_obj.status == PublishStatus.PENDING
