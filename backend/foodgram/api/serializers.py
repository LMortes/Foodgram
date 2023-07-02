from djoser.serializers import UserSerializer, UserCreateSerializer
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from .image_field_serializer import Base64ImageField
from recipes.models import (Tag, Recipe, IngredientInRecipe,
                            ShoppingCart, Favorite, Ingredient)
from users.models import User, Subscription


class UserProfileGetSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        return Subscription.objects.filter(
            author=obj,
            user=request.user
        ).exists()


class UserRecipesSerializer(UserProfileGetSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = UserProfileGetSerializer.Meta.fields + (
            'recipes',
            'recipes_count'
        )

    def validate(self, data):
        author = self.instance
        user = self.context.get('request').user
        if Subscription.objects.filter(author=author, user=user).exists():
            raise ValidationError(
                detail='Эх! Ты уже подписан на этого автора, \
                второй раз нельзя(',
                code=status.HTTP_400_BAD_REQUEST
            )
        if user == author:
            raise ValidationError(
                detail='Эх! Нельзя стать подписчиком самого себя',
                code=status.HTTP_400_BAD_REQUEST
            )
        return data

    def get_recipes(self, object):
        request = self.context.get('request')
        context = {'request': request}
        recipe_limit = request.query_params.get('recipe_limit')
        queryset = object.recipes.all()
        if recipe_limit:
            queryset = queryset[:int(recipe_limit)]
        return RecipeMiniSerializer(queryset, context=context, many=True).data

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class UserNewSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password'
        )


class SubscriptionSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Subscription
        fields = ('author', 'user')
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Subscription.objects.all(),
                fields=[
                    'author',
                    'user'
                ],
                message="Эх! Ты уже подписан на этого автора, \
                второй раз нельзя("
            )
        ]

    def create(self, validated_data):
        return Subscription.objects.create(
            user=self.context.get('request').user,
            **validated_data
        )

    def validate_author(self, value):
        if self.context.get('request').user == value:
            raise serializers.ValidationError({
                'errors': 'Эх! Нельзя стать подписчиком самого себя'
            })
        return value


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'metric')


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        source='ingredient.id'
    )
    name = serializers.CharField(
        source='ingredient.name',
        read_only=True
    )
    metric = serializers.CharField(
        source='ingredient.metric',
        read_only=True
    )

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'metric', 'amount')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class RecipeGetSerializer(serializers.ModelSerializer):
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    tags = TagSerializer(many=True, read_only=True)
    author = UserProfileGetSerializer()
    ingredients = IngredientInRecipeSerializer(
        source='IngredientsInRecipe',
        many=True,
        read_only=True
    )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        return Favorite.objects.filter(recipe=obj, user=request.user).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(
            recipe=obj,
            user=request.user
        ).exists()


class RecipeMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class RecipeCreateSerializer(serializers.ModelSerializer):
    author = UserProfileGetSerializer(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    ingredients = IngredientInRecipeSerializer(
        source='IngredientsInRecipe',
        many=True
    )
    image = Base64ImageField(
        required=False,
        allow_null=True
    )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    @staticmethod
    def save_ingredients(recipe, ingredients):
        ingredients_list = []
        for ingredient in ingredients:
            current_ingredient = ingredient['ingredient']['id']
            current_amount = ingredient.get('amount')
            ingredients_list.append(
                IngredientInRecipe(
                    recipe=recipe,
                    ingredient=current_ingredient,
                    amount=current_amount
                )
            )
        IngredientInRecipe.objects.bulk_create(ingredients_list)

    def validate_ingredients(self, data):
        ingredients_list = []
        ingredients_in_recipe = data.get('IngredientsInRecipe')
        for ingredient in ingredients_in_recipe:
            ingredients_list.append(ingredient['ingredient']['id'])
        if len(ingredients_list) > len(set(ingredients_list)):
            raise serializers.ValidationError(
                {
                    'error': 'В рецепте ингридиенты не могут повторяться'
                }
            )
	return data

    def validate_tags(self, data):
        tags = data['tags']
        if not tags:
            raise serializers.ValidationError(
                {
                    'error': 'Нужен хотя бы один тэг для рецепта!'
                }
            )
        tag_names = [tag.name for tag in tags]
        if len(tag_names) != len(set(tag_names)):
            raise serializers.ValidationError(
                {
                    'error': 'Тэги не могут повторяться!'
                }
            )
	return data

    def validate(self, data):
        self.validate_ingredients(data)
        self.validate_tags(data)

        return data

    def create(self, validated_data):
        author = self.context.get('request').user
        ingredients = validated_data.pop('IngredientsInRecipe')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data, author=author)
        recipe.tags.add(*tags)
        self.save_ingredients(recipe, ingredients)
	recipe.save()
        return recipe

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.image = validated_data.get('image', instance.image)
        instance.cooking_time = validated_data.get(
            'cooking_time',
            instance.cooking_time
        )
        ingredients = validated_data.pop('IngredientsInRecipe')
        tags = validated_data.pop('tags')
        instance.tags.clear()
        instance.tags.add(*tags)
        instance.ingredients.clear()
        recipe = instance
        self.save_ingredients(recipe, ingredients)
        return instance

    def to_representation(self, instance):
        serializer = RecipeGetSerializer(
            instance,
            context={
                'request': self.context.get('request')
            }
        )
        return serializer.data


class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    recipe = serializers.PrimaryKeyRelatedField(
        queryset=Recipe.objects.all(),
        write_only=True
    )

    class Meta:
        model = Favorite
        fields = ('recipe', 'user')
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=['recipe', 'user'],
                message='Данный рецепт уже есть у вас в избранном'
            )
        ]

    def create(self, validated_data):
        return Favorite.objects.create(
            user=self.context.get('request').user, **validated_data)


class ShoppingCartSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    recipe = serializers.PrimaryKeyRelatedField(
        queryset=Recipe.objects.all(),
        write_only=True
    )

    class Meta:
        model = ShoppingCart
        fields = ('recipe', 'user',)
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=ShoppingCart.objects.all(),
                fields=['recipe', 'user', ],
                message='Данный рецепт уже есть у вас в корзине'
            )
        ]

    def create(self, validated_data):
        return ShoppingCart.objects.create(
            user=self.context.get('request').user,
            **validated_data
        )
