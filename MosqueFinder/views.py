from django.contrib.auth.models import User
from django.db.backends.utils import logger
from rest_framework import permissions, generics
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegisterSerializer, UpdatePasswordSerializer, UpdateUserSerializer, \
    LocationSerializer


# view to sign up for the app
class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        logger.info("RegisterView: post" + str(request.data))
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("RegisterView: post: serializer is valid")
            logger.info("RegisterView: post: serializer.data: " + str(serializer.data))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.info("RegisterView: post: serializer is not valid")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# update password view
class UpdatePasswordView(RetrieveAPIView):
    serializer_class = UpdatePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        logger.info("UpdatePasswordView: put: request.data: " + str(request.data))
        serializer = UpdatePasswordSerializer(data=request.data)
        if serializer.is_valid():
            logger.info("UpdatePasswordView: put: serializer is valid")
            logger.info("UpdatePasswordView: put: serializer.data: " + str(serializer.data))
            serializer.update(request.user, serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        logger.info("UpdatePasswordView: put: serializer is not valid")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# update the user details
class UpdateUserView(RetrieveAPIView):
    serializer_class = UpdateUserSerializer
    permission_classes = [permissions.IsAuthenticated]
    def put(self, request):
        logger.info("UpdateUserView: put: request.data: " + str(request.data))
        serializer = UpdateUserSerializer(data=request.data)
        if serializer.is_valid():
            logger.info("UpdateUserView: put: serializer is valid")
            user = serializer.update(request.user, serializer.validated_data)
            return Response(User.objects.get(username=user).username, status=status.HTTP_200_OK)
        logger.info("UpdateUserView: put: serializer is not valid")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# takes a post request with a point and updates the user's last location
# the data is in the form of a json object
class UpdateLocation(generics.UpdateAPIView):
    """
    API endpoint that allows for updating the location of the user by updating the last_location field
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        logger.info("UpdateLocation: post: request.data: " + str(request.data))
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            logger.info("UpdateLocation: post: serializer is valid")
            logger.info("UpdateLocation: post: serializer.data: " + str(serializer.validated_data))
            user = serializer.update(request.user, serializer.validated_data)
            return Response(User.objects.get(username=user).username, status=status.HTTP_200_OK)
        logger.info("UpdateLocation: post: serializer is not valid")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
