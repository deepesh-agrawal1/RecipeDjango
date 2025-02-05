from ninja import Router
from .models import Recipe, FavoriteRecipe
from django.shortcuts import get_object_or_404
from typing import List
from pydantic import BaseModel

recipeRouter = Router()

class RecipeSchema(BaseModel):
    name: str
    ingredients: str
    cooking_steps: str
    preparation_time: int
    servings: int
    difficulty: str

class RecipeOutSchema(RecipeSchema):
    id: int

class FavoriteRecipeSchema(BaseModel):
    user: str  # Ideally, this should be taken from authentication context
    recipe_id: int

@recipeRouter.get("/", response=List[RecipeOutSchema])
def get_recipes(request):
    recipes = Recipe.objects.all()
    return [RecipeOutSchema.model_validate(recipe.__dict__) for recipe in recipes]

@recipeRouter.post("/", response=RecipeOutSchema)
def add_recipe(request, payload: RecipeSchema):
    recipe = Recipe.objects.create(**payload.dict())
    return RecipeOutSchema.model_validate(recipe.__dict__)

@recipeRouter.get("/{recipe_id}", response=RecipeOutSchema)
def get_recipe(request, recipe_id: int):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return RecipeOutSchema.model_validate(recipe.__dict__)

@recipeRouter.put("/{recipe_id}", response=RecipeOutSchema)
def update_recipe(request, recipe_id: int, payload: RecipeSchema):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    for attr, value in payload.dict().items():
        setattr(recipe, attr, value)
    recipe.save()
    return RecipeOutSchema.model_validate(recipe.__dict__)

@recipeRouter.delete("/{recipe_id}")
def delete_recipe(request, recipe_id: int):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    recipe.delete()
    return {"message": "Recipe deleted successfully!"}

@recipeRouter.post("/favorite/")
def add_favorite_recipe(request, payload: FavoriteRecipeSchema):
    recipe = get_object_or_404(Recipe, id=payload.recipe_id)
    favorite, created = FavoriteRecipe.objects.get_or_create(user=payload.user, recipe=recipe)
    if created:
        return {"message": "Recipe added to favorites!"}
    return {"message": "Recipe is already in favorites!"}

@recipeRouter.get("/favorite/{user}", response=List[RecipeOutSchema])
def get_favorite_recipes(request, user: str):
    favorites = FavoriteRecipe.objects.filter(user=user).values_list("recipe_id", flat=True)
    recipes = Recipe.objects.filter(id__in=favorites)
    return [RecipeOutSchema.model_validate(recipe.__dict__) for recipe in recipes]

@recipeRouter.delete("/favorite/{user}/{recipe_id}")
def remove_favorite_recipe(request, user: str, recipe_id: int):
    favorite = get_object_or_404(FavoriteRecipe, user=user, recipe_id=recipe_id)
    favorite.delete()
    return {"message": "Recipe removed from favorites!"}
