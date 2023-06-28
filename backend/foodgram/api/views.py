from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import F, Sum
from rest_framework import viewsets, status, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from djoser.serializers import SetPasswordSerializer
from users.models import User, Subscription
from recipes.models import (Tag, Recipe, Favorite,
                            ShoppingCart, IngredientInRecipe,
                            Ingredient)
from .serializers import (IngrSerializer, TagSerializer,
                          RecipeGetSerializer, FavoriteSerializer,
                          RecipeCreateSerializer, RecipeMiniSerializer,
                          ShoppingCartSerializer, UserProfileGetSerializer,
                          UserNewSerializer, SubscriptionSerializer,
                          UserRecipesSerializer)
from .permissions import IsAuthorOrAdminOrReadOnly
from .pagination import CustomPagination
from .filters import RecipeFilter, IngrFilter
from .utils import create_and_delete


class ModernUserViewSet(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    queryset = User.objects.all()
    pagination_class = CustomPagination

    def get_instance(self):
        return self.request.user

    def get_serializer_class(self):
        if self.action in ['subscriptions', 'subscribe']:
            return UserRecipesSerializer
        elif self.request.method == 'GET':
            return UserProfileGetSerializer
        elif self.request.method == 'POST':
            return UserNewSerializer

    def get_permissions(self):
        if self.action == 'retrieve':
            self.permission_classes = [IsAuthenticated]
        return super(self.__class__, self).get_permissions()

    @action(
        detail=False,
        permission_classes=[IsAuthenticated],
    )
    def me(self, request, *args, **kwargs):
        self.get_object = self.get_instance
        return self.retrieve(request, *args, **kwargs)

    @action(
        ["POST"],
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def set_password(self, request, *args, **kwargs):
        serializer = SetPasswordSerializer(
            data=request.data, context={
                'request': request
            }
        )
        serializer.is_valid(raise_exception=True)
        self.request.user.set_password(serializer.data['new_password'])
        self.request.user.save()
        update_session_auth_hash(self.request, self.request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def subscriptions(self, request):
        users = User.objects.filter(
            following__user=request.user
        ).prefetch_related('recipes')
        page = self.paginate_queryset(users)
        if page is not None:
            serializer = UserRecipesSerializer(
                page, many=True,
                context={
                    'request': request
                }
            )
            return self.get_paginated_response(serializer.data)
        serializer = UserRecipesSerializer(
            users,
            many=True,
            context={
                'request': request
            }
        )
        return Response(serializer.data)

    @action(
        ["POST", "DELETE"],
        detail=True,
        permission_classes=[IsAuthorOrAdminOrReadOnly],
    )
    def subscribe(self, request, **kwargs):
        return create_and_delete(
            self,
            request,
            User,
            Subscription,
            SubscriptionSerializer,
            **kwargs
        )


class IngrViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngrSerializer
    filter_backends = (DjangoFilterBackend)
    filterset_class = IngrFilter
    pagination_class = None


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthorOrAdminOrReadOnly]
    filter_backends = (DjangoFilterBackend)
    filterset_class = RecipeFilter
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeGetSerializer
        elif self.action in ['favorite', 'shopping_cart', ]:
            return RecipeMiniSerializer
        return RecipeCreateSerializer

    @action(
        ["POST", "DELETE"],
        detail=True
    )
    def favorite(self, request, **kwargs):
        return create_and_delete(
            self,
            request,
            Recipe,
            Favorite,
            FavoriteSerializer,
            **kwargs
        )

    @action(
        ["POST", "DELETE"],
        detail=True
    )
    def shopping_cart(self, request, **kwargs):
        return create_and_delete(
            self,
            request,
            Recipe,
            ShoppingCart,
            ShoppingCartSerializer,
            **kwargs
        )

    @action(
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        user = request.user
        ingredients = IngredientInRecipe.objects.filter(
            recipe__shopping_cart__user=user).values(
            name=F('ingredient__name'),
            metric=F('ingredient__metric')).annotate(
            amount=Sum('amount')
        )
        data = []
        for ingredient in ingredients:
            data.append(
                f'{ingredient["name"]} - '
                f'{ingredient["amount"]} '
                f'{ingredient["metric"]}'
            )
        content = 'Список покупок:\n\n' + '\n'.join(data)
        filename = 'Shopping_cart.txt'
        request = HttpResponse(content, content_type='text/plain')
        request['Content-Disposition'] = f'attachment; filename={filename}'
        return request
