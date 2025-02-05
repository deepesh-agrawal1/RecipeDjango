from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI
from recipes.api import recipeRouter

api = NinjaAPI()
api.add_router("/recipes/", recipeRouter)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),
]
