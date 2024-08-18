from pathlib import Path

from recipy.json import recipe_from_json


def test_recipe_from_json():
    failures = []
    for json_file in Path(__file__).parent.glob('test_data/*.json'):
        with open(json_file, 'r') as f:
            recipe = recipe_from_json(f.read())
            if recipe is None:
                failures.append(json_file)
    assert not failures, f"Failed on {failures}"
