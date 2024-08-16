# Recipy

Recipy extracts recipes from web pages using JSON-LD and converts them into Python objects. It also supports generating Markdown, LaTeX, and PDFs.

```python
from recipy.microdata import recipe_from_url

url = "https://www.allrecipes.com/recipe/14231/guacamole/"
recipe = recipe_from_url(url)
if recipe:
    print(recipe.model_dump())
```

## Installation

### Install via pip

```bash
pip install python-recipy
```

### Install `texlive` for PDF Generation

#### Debian/Ubuntu

```bash
sudo apt install texlive
```

#### macOS
    
```bash
brew install texlive
```

## Examples

### Load Recipe from JSON

```python
from recipy.microdata import recipe_from_json

json_data = '''
{
    "name": "Tomato Basil Salad",
    "recipeIngredient": ["2 ripe tomatoes, sliced", "1/4 cup fresh basil leaves, torn"],
    "recipeInstructions": [
        {
            "@type": "HowToSection",
            "name": "Making the Salad",
            "itemListElement": [
                {"@type": "HowToStep", "text": "Arrange the tomato slices on a plate."},
                {"@type": "HowToStep", "text": "Scatter the torn basil leaves over the tomatoes."}
            ]
        },
        {
            "@type": "HowToSection",
            "name": "Preparing the Dressing",
            "itemListElement": [
                {"@type": "HowToStep", "text": "In a small bowl, whisk together the olive oil and balsamic vinegar."},
                {"@type": "HowToStep", "text": "Drizzle the dressing over the tomatoes and basil before serving."}
            ]
        }
    ]
}
'''

recipe = recipe_from_json(json_data)
if recipe:
    print(recipe.model_dump())
```

### Parse Recipe from Markdown

```python
from recipy.markdown import recipe_from_markdown

markdown_content = """
# Tomato Basil Salad

A simple and fresh tomato basil salad.

## Ingredients

### For the Salad

* 2 ripe tomatoes, sliced
* 1/4 cup fresh basil leaves, torn

### For the Dressing

* 2 tablespoons olive oil
* 1 tablespoon balsamic vinegar

## Instructions

### Making the Salad

1. Arrange the tomato slices on a plate.
2. Scatter the torn basil leaves over the tomatoes.

### Preparing the Dressing

1. In a small bowl, whisk together the olive oil and balsamic vinegar.
2. Drizzle the dressing over the tomatoes and basil before serving.

## Notes

Serve immediately for the best flavor.
"""

recipe = recipe_from_markdown(markdown_content)
if recipe:
    print(recipe.model_dump())
```

#### Markdown Structure

* The recipe title must be an H1 (`# Title`).
* Ingredients must be under an H2 heading `## Ingredients`, with optional H3 subheadings for ingredient groups.
* Instructions must be under an H2 heading `## Instructions`, with optional H3 subheadings for instruction groups.
* Notes can be included under an H2 heading `## Notes`.

### Convert Recipe to PDF

```python
from recipy.pdf import recipe_to_pdf
from recipy.models import Recipe, IngredientGroup, InstructionGroup

recipe = Recipe(
    title="Tomato Basil Salad",
    description="A simple and fresh tomato basil salad.",
    ingredient_groups=[
        IngredientGroup(name="For the Salad", ingredients=["2 ripe tomatoes, sliced", "1/4 cup fresh basil leaves, torn"]),
        IngredientGroup(name="For the Dressing", ingredients=["2 tablespoons olive oil", "1 tablespoon balsamic vinegar"])
    ],
    instruction_groups=[
        InstructionGroup(name="Making the Salad", instructions=["Arrange the tomato slices on a plate.", "Scatter the torn basil leaves over the tomatoes."]),
        InstructionGroup(name="Preparing the Dressing", instructions=["In a small bowl, whisk together the olive oil and balsamic vinegar.", "Drizzle the dressing over the tomatoes and basil before serving."])
    ]
)

pdf_content = recipe_to_pdf(recipe)
with open("recipe.pdf", "wb") as f:
    f.write(pdf_content)
```

### Convert Recipe to LaTeX

```python
from recipy.latex import recipe_to_latex
from recipy.models import Recipe, IngredientGroup, InstructionGroup

recipe = Recipe(
    title="Tomato Basil Salad",
    description="A simple and fresh tomato basil salad.",
    ingredient_groups=[
        IngredientGroup(name="For the Salad", ingredients=["2 ripe tomatoes, sliced", "1/4 cup fresh basil leaves, torn"]),
        InstructionGroup(name="For the Dressing", ingredients=["2 tablespoons olive oil", "1 tablespoon balsamic vinegar"])
    ],
    instruction_groups=[
        InstructionGroup(name="Making the Salad", instructions=["Arrange the tomato slices on a plate.", "Scatter the torn basil leaves over the tomatoes."]),
        InstructionGroup(name="Preparing the Dressing", instructions=["In a small bowl, whisk together the olive oil and balsamic vinegar.", "Drizzle the dressing over the tomatoes and basil before serving."])
    ]
)

latex_content = recipe_to_latex(recipe)
print(latex_content)
```
