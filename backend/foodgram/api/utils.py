from django.shortcuts import get_object_or_404
from recipes.models import Recipe
from users.models import User
from rest_framework.response import Response
from rest_framework import status


def create_and_delete(
        self,
        request,
        model_1,
        model_2,
        serializer,
        **kwargs):
    obj_1 = get_object_or_404(model_1, id=kwargs['pk'])
    data = request.data.copy()
    if model_1 == Recipe:
        data.update({
            'recipe': obj_1.id
        })
    elif model_1 == User:
        data.update({
            'author': obj_1.id
        })
    serializer = serializer(
        data=data, context={
            'request': request
        }
    )
    if request.method == "POST":
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            status=status.HTTP_201_CREATED,
            data=self.get_serializer(obj_1).data
        )
    elif request.method == "DELETE" and model_1 == Recipe:
        object = model_2.objects.filter(
            recipe=obj_1,
            user=request.user
        )
        if not object.exists():
            return Response({
                'errors': 'Этого рецепта нет в вашем списке покупок"'},
                status=status.HTTP_400_BAD_REQUEST
            )
        object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == "DELETE" and model_1 == User:
        object = model_2.objects.filter(
            author=obj_1,
            user=request.user
        )
        if not object.exists():
            return Response(
                {
                    'errors': 'Эх! К сожалению, ты не \
                    подписан на этого пользователя'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
