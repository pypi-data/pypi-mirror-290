import json
from dataclasses import asdict

from recipy.microdata import recipe_from_url


def test_recipe_from_url():
    recipe = recipe_from_url('https://www.allrecipes.com/recipe/17481/simple-white-cake/')
    print(recipe.model_dump_json(indent=2))
    # TODO: Assert that the recipe is correct


def test_recipe_from_url_text():
    recipe = recipe_from_url('https://smittenkitchen.com/2024/07/braised-chickpeas-with-zucchini-and-pesto/')
    pass


def test_recipe_from_json_with_string():
    # TODO: Load fixture from file and test
    pass
