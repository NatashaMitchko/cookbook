from app.model.recipe import Recipe, PublishStatus

def test_recipe_initialization():
    recipe = Recipe(
        "new recipe",
        "i-am-a-slug",
        "",
        ["1 carrot", "2 peas"],
        ["cook 'em"],
        ["dinner"],
        PublishStatus.PENDING
    )
    assert recipe.title == "New Recipe"
    assert type(recipe.status) == PublishStatus
