from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (IngredientViewSet, TagViewSet,
                    RecipeViewSet, ModernUserViewSet)

app_name = 'api'

router = DefaultRouter()
router.register('users', ModernUserViewSet, basename='users')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('tags', TagViewSet, basename='tags')
router.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
