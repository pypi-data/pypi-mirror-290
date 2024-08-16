# import json
# from dataclasses import asdict
#
# from recipy.markdown import recipe_from_markdown, recipe_to_markdown
# from recipy.microdata import recipe_from_url
# from recipy.latex import recipe_to_latex
# from recipy.pdf import recipe_to_pdf
#
#
# def test():
#     recipe = recipe_from_url('https://www.allrecipes.com/recipe/17481/simple-white-cake/')
#     print(json.dumps(asdict(recipe), indent=4))
#
#     recipe_markdown = recipe_to_markdown(recipe)
#     print(recipe_markdown)
#
#     recipe_markdown = """# Simple White Cake
#
# ## Ingredients
#
# ### For the Cake
#
# * 1 cup white sugar
# * 0.5 cup unsalted butter
# * 2 large eggs
# * 2 teaspoons vanilla extract
# * 1.5 cups all-purpose flour
# * 1.75 teaspoons baking powder
# * 0.5 cup milk
#
# ### For the Frosting
#
# * 1/2 cup unsalted butter
# * 2 cups confectioners' sugar
# * 1 teaspoon vanilla extract
# * 1 tablespoon milk
#
# ## Instructions
#
# ### Make the Cake
#
# 1. Gather all ingredients.
# 2. Preheat the oven to 350 degrees F (175 degrees C). Grease and flour a 9-inch square cake pan.
# 3. Cream sugar and butter together in a mixing bowl. Add eggs, one at a time, beating briefly after each addition. Mix in vanilla.
# 4. Combine flour and baking powder in a separate bowl. Add to the wet ingredients and mix well. Add milk and stir until smooth.
# 5. Pour batter into the prepared cake pan.
# 6. Bake in the preheated oven until the top springs back when lightly touched, 30 to 40 minutes.
# 7. Remove from the oven and cool completely.
#
# ### Make the Frosting
#
# 1. Cream butter in a bowl. Add confectioners' sugar, vanilla extract, and milk. Beat until smooth.
#
# ### Assemble the Cake
#
# 1. Spread frosting over cooled cake.
# 2. Slice and serve.
# 3. Enjoy!"""
#     recipe = recipe_from_markdown(recipe_markdown)
#     pdf = recipe_to_pdf(recipe)
#     with open('recipe.pdf', 'wb') as f:
#         f.write(pdf)
#
#     latex = recipe_to_latex(recipe)
#     print(latex)
#
#
# if __name__ == '__main__':
#     test()
