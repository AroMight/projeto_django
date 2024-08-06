from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from authors.serializers import AuthorSerializer
from django.contrib.auth.models import User
from rest_framework import status


class AuthorAPIv2ViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AuthorSerializer

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        user = User(**data)
        user.set_password(data['password'])
        user.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        # data = request.data

        # user = User(**data)
        # user.set_password(data['password'])
        # user.save()

        # serializer = self.get_serializer(user)
        # headers = self.get_success_headers(serializer.data)
        # return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
