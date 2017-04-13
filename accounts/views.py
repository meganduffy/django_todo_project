from __future__ import unicode_literals
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import UserSerializer


class UserView(APIView):
    """
    UserView handles the requests made to '/accounts/'
    """

    permission_classes = ()
    serializer_class = UserSerializer

    def post(self, request):
        """
        Handles the POST request made to the '/accounts/' URL.

        This view will take the 'data' property from the 'request' object,
        deserialize it into a 'User' object and store in the DB.

        Returns a 201 (successfully created) if the user is successfully
        created, otherwise returns a 400 (bad request)
        """
        serializer = UserSerializer(data=request.data)

        # Check to see if the data in the 'request' is valid.
        # If the item can not be deserialized into a 'Todo' object then
        # a bad request response will be returned.
        # Else, save the data and return the data and a successfully
        # created status.
        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        else:
            data = serializer.data

            # Create a new user using the 'username' contained in
            # the 'data' dict
            user = User.objects.create(username=data['username'])
            user.set_password(data['password'])
            # Finally, save the new 'user' object
            user.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
