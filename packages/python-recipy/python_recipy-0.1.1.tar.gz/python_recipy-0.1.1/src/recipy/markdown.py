from typing import Optional, List
from xml.etree.ElementTree import Element

import markdown
from markdown import Extension
from markdown.treeprocessors import Treeprocessor

from . import utils
from .models import Recipe, IngredientGroup, InstructionGroup, Review, Meta, Rating


def recipe_from_markdown(content: str) -> Optional[Recipe]:
    recipe_extension = RecipeExtension()
    md = markdown.Markdown(extensions=[recipe_extension])

    try:
        _ = md.convert(content)
        recipe = recipe_extension.recipe_parser.recipe
        if recipe:
            return recipe
        else:
            return None
    except ValueError as e:
        print(f"Failed to parse recipe: {str(e)}")
        return None


class RecipeParser(Treeprocessor):
    def run(self, root: Element):
        self.recipe = self.parse_recipe(root)
        if self.recipe is None:
            raise ValueError("Markdown structure does not conform to expected format")
        return root  # We still need to return the root for other processors

    def parse_recipe(self, root: Element) -> Optional[Recipe]:
        if len(root) == 0 or root[0].tag != 'h1':
            return None

        title = root[0].text
        current_index = 1
        description = None

        if len(root) > current_index and root[current_index].tag == 'p':
            description = root[current_index].text
            current_index += 1

        if len(root) <= current_index or root[current_index].tag != 'h2' or root[current_index].text != 'Ingredients':
            return None

        current_index += 1
        ingredient_groups = self.parse_ingredient_groups(root, current_index)
        if ingredient_groups is None:
            return None

        # Find the Instructions heading
        while current_index < len(root) and (root[current_index].tag != 'h2' or root[current_index].text != 'Instructions'):
            current_index += 1

        if current_index >= len(root):
            return None

        current_index += 1
        instruction_groups = self.parse_instruction_groups(root, current_index)
        if instruction_groups is None:
            return None

        current_index += 1
        notes = None
        if current_index < len(root) and root[current_index].tag == 'h2' and root[current_index].text == 'Notes':
            notes = root[current_index + 1].text
            current_index += 2

        # Initialize new fields with default values
        reviews = []
        image_url = None
        rating = None
        meta = None

        return Recipe(
            title=title,
            description=description,
            ingredient_groups=ingredient_groups,
            instruction_groups=instruction_groups,
            notes=notes,
            reviews=reviews,
            image_url=image_url,
            rating=rating,
            meta=meta
        )

    def parse_ingredient_groups(self, root, start_index) -> Optional[List[IngredientGroup]]:
        groups = []
        current_index = start_index

        while current_index < len(root) and root[current_index].tag != 'h2':
            if root[current_index].tag == 'h3':
                name = root[current_index].text
                current_index += 1
                if len(root) <= current_index or root[current_index].tag != 'ul':
                    return None
                ingredients = [utils.normalize_fractions(li.text) for li in root[current_index] if li.tag == 'li']
                groups.append(IngredientGroup(name=name, ingredients=ingredients))
                current_index += 1
            elif root[current_index].tag == 'ul':
                ingredients = [utils.normalize_fractions(li.text) for li in root[current_index] if li.tag == 'li']
                groups.append(IngredientGroup(name=None, ingredients=ingredients))
                current_index += 1
            else:
                current_index += 1

        return groups if groups else None

    def parse_instruction_groups(self, root, start_index) -> Optional[List[InstructionGroup]]:
        groups = []
        current_index = start_index

        while current_index < len(root):
            if root[current_index].tag == 'h3':
                name = root[current_index].text
                current_index += 1
                if len(root) <= current_index or root[current_index].tag != 'ol':
                    return None
                instructions = [utils.normalize_fractions(li.text) for li in root[current_index] if li.tag == 'li']
                groups.append(InstructionGroup(name=name, instructions=instructions))
                current_index += 1
            elif root[current_index].tag == 'ol':
                instructions = [utils.normalize_fractions(li.text) for li in root[current_index] if li.tag == 'li']
                groups.append(InstructionGroup(name=None, instructions=instructions))
                current_index += 1
            else:
                break

        return groups if groups else None


class RecipeExtension(Extension):
    def __init__(self):
        self.recipe_parser = None
        super().__init__()

    def extendMarkdown(self, md):
        self.recipe_parser = RecipeParser(md)
        md.treeprocessors.register(self.recipe_parser, 'recipeparser', 15)


def recipe_to_markdown(recipe: Recipe):
    md = f"# {recipe.title}\n\n"

    if recipe.description:
        md += f"{recipe.description}\n\n"

    md += "## Ingredients\n\n"
    for ingredient_group in recipe.ingredient_groups:
        if ingredient_group.name:
            md += f"### {ingredient_group.name}\n\n"
        for ingredient in ingredient_group.ingredients:
            md += f"* {ingredient}\n"
        md += "\n"

    md += "## Instructions\n\n"
    for instruction_group in recipe.instruction_groups:
        if instruction_group.name:
            md += f"### {instruction_group.name}\n\n"
        for i, instruction in enumerate(instruction_group.instructions, 1):
            md += f"{i}. {instruction}\n"
        md += "\n"

    return md.strip() + "\n"
