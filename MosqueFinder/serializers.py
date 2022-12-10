from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point
from rest_framework import serializers

from .models import WorldBorder, Profile


class WorldBorderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WorldBorder
        fields = ['name', 'area', 'pop2005', 'fips', 'iso2', 'iso3', 'un', 'region', 'subregion', 'lon', 'lat', 'mpoly']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username']


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user


class UpdatePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['password']
        extra_kwargs = {'password': {'write_only': True}}

    def update(self, instance, validated_data):
        user = get_user_model().objects.get(username=instance)
        user.set_password(validated_data['password'])
        user.save()
        return user


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email']

    def update(self, instance, validated_data):
        user = get_user_model().objects.get(username=instance)
        user.first_name = validated_data['first_name']
        user.last_name = validated_data['last_name']
        user.email = validated_data['email']
        user.save()
        return user


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['last_location']

    def update(self, instance, validated_data):
        user_profile = Profile.objects.get(user=instance)
        lat = self.initial_data['lat']
        lon = self.initial_data['lon']
        point = Point(float(lon), float(lat))
        user_profile.last_location = point
        user_profile.save()
        return user_profile

