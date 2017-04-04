from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import TodoSerializer
from .models import Todo
from django.contrib.auth.models import User


class TodoView(APIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = TodoSerializer

    def get(self, request, pk=None):
        if "username" in request.query_params:

            if pk is not None:
                todo = Todo.objects.get(id=pk)
                serializer = TodoSerializer(todo)
            else:
                user = User.objects.get(username=request.query_params["username"])
                todos = Todo.objects.filter(user=user)
                serializer = TodoSerializer(todos, many=True)

            return Response(serializer.data)

        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = TodoSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        data = serializer.data

        user = User.objects.get(username=data["username"])

        Todo.objects.create(user=user, title=data["title"],
                            description=data["description"], status=data["status"])

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, pk):
        todo = Todo.objects.get(id=pk)
        serializer = TodoSerializer(todo, data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        todo = Todo.objects.get(id=pk)
        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
