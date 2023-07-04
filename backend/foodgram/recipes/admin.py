from django.contrib import admin
from .models import (Recipe, Tag, IngredientInRecipe,
                     ShoppingCart, Favorite, Ingredient)


class RecipeIngrInline(admin.TabularInline):
    model = IngredientInRecipe
    min_num = 1
    extra = 0


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngrInline, )
    list_display = (
        'name',
        'author',
        'pub_date'
    )
    list_filter = ('name', 'author', )
    search_fields = ('name', )


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe'
    )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'slug',
        'color'
    )


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe'
    )


@admin.register(Ingredient)
class IngrAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'measurement_unit'
    )


@admin.register(IngredientInRecipe)
class IngrInRecipeAdmin(admin.ModelAdmin):
    list_display = (
        'recipe',
        'ingredient',
        'amount'
    )
