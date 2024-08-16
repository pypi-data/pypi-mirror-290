from typing import Optional, List
from pydantic import BaseModel, Field

class IngredientGroup(BaseModel):
    name: Optional[str]
    ingredients: List[str]

class InstructionGroup(BaseModel):
    name: Optional[str]
    instructions: List[str]

class Review(BaseModel):
    author: Optional[str]
    body: Optional[str]
    rating: Optional[float]

class Meta(BaseModel):
    prep_time_minutes: Optional[int]
    cook_time_minutes: Optional[int]
    total_time_minutes: Optional[int]
    recipe_yield: Optional[str]

class Rating(BaseModel):
    value: Optional[float] = Field(0)
    count: Optional[int] = Field(0)

class Recipe(BaseModel):
    title: str
    description: Optional[str]
    ingredient_groups: List[IngredientGroup] = Field(default_factory=list)
    instruction_groups: List[InstructionGroup] = Field(default_factory=list)
    notes: Optional[str] = None
    reviews: List[Review] = Field(default_factory=list)
    image_url: Optional[str] = None
    rating: Optional[Rating] = None
    meta: Optional[Meta] = None
