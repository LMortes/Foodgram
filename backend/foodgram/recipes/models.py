from django.db import models
from django.core.validators import MinValueValidator, RegexValidator
from users.models import User


class Ingredient(models.Model):
    name = models.CharField(
        'Имя ингридиента',
        max_length=100
    )
    metric = models.CharField(
        'Единица измерения ингридиента',
        max_length=30
    )

    class Meta:
        verbose_name = 'ингредиент'
        verbose_name_plural = 'ингредиенты'

    def __str__(self):
        return f'{self.name} в {self.metric}'


class Tag(models.Model):
    name = models.CharField(
        'Тэг',
        max_length=150,
        unique=True
    )
    slug = models.SlugField(
        db_index=True,
        unique=True
    )
    color = models.CharField(
        'Цвет тэга',
        max_length=7,
        validators=[
            RegexValidator(
                regex='^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',
                message='Цвет должен быть задан в формате HEX, \
                например #FFFFFF'
            )
        ]
    )

    class Meta:
        verbose_name = 'тэг'
        verbose_name_plural = 'тэги'

    def __str__(self):
        return self.slug


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    name = models.CharField(
        'Имя рецепта',
        max_length=100
    )
    image = models.ImageField(
        'Иконка',
        upload_to='recipes/images/'
    )
    text = models.TextField('Описание рецепта')
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientInRecipe',
        related_name='recipes'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes'
    )
    cooking_time = models.IntegerField(
        'Время приготовления(мин.)',
        validators=[
            MinValueValidator(
                1, 'Время приготовления начинается от 1 минуты'
            )
        ]
    )
    pub_date = models.DateTimeField(
        'Дата создания рецепта',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'
        ordering = ['-pub_date']

    def __str__(self):
        return self.name


class IngredientInRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='IngredientsInRecipe'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='IngredientsInRecipe'
    )
    amount = models.IntegerField(
        'Кол-во ингридиентов в 1 рецепте',
        validators=[
            MinValueValidator(
                1, 'Меньше одного ингридиента быть не может'
            )
        ]
    )

    class Meta:
        verbose_name = 'ингридиент в рецепте'
        verbose_name_plural = 'ингридиенты в рецепте'

    def __str__(self):
        return f'{self.ingredient.name} в рецепте {self.recipe.name}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='FavoriteRecipe'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='FavoriteRecipe'
    )

    class Meta:
        verbose_name = 'избранный рецепт'
        verbose_name_plural = 'избранные рецепты'

    def __str__(self):
        return f'{self.recipe.name} в списке избанного у {self.user.username}'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='RecipeInShoppingList'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart'
    )

    class Meta:
        verbose_name = 'рецепт в корзине'
        verbose_name_plural = 'рецепты в корзине'

    def __str__(self):
        return f'{self.recipe.name} в корзине у {self.user.username}'
