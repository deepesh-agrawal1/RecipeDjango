from django.db import models

class Recipe(models.Model):
    name = models.CharField(max_length=255)
    ingredients = models.TextField()
    cooking_steps = models.TextField()
    preparation_time = models.IntegerField(help_text="Time in minutes", default=30)
    servings = models.IntegerField(default=1)
    difficulty = models.CharField(
        max_length=20, choices=[("Easy", "Easy"), ("Medium", "Medium"), ("Hard", "Hard")], default="Easy"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class FavoriteRecipe(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="favorites")
    user = models.CharField(max_length=255)  # Ideally, use a ForeignKey to User model if using authentication.

    def __str__(self):
        return f"{self.user} - {self.recipe.name}"
