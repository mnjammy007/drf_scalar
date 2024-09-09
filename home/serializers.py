from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from rest_framework import serializers

from .models import Person, Color


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=100)

    class Meta:
        exclude = ["password"]


class LogoutSerializer(serializers.Serializer):
    token = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(max_length=100)

    def validate(self, attrs):
        try:
            user_from_auth = authenticate(
                username=attrs.get("email"),
                password=attrs.get("password"),
            )
            user_from_token = User.objects.get(auth_token=attrs.get("token"))
            if not user_from_auth or not user_from_token:
                raise serializers.ValidationError("Invalid Token or credentials.")
            if user_from_auth.email != user_from_token.email:
                raise serializers.ValidationError("Invalid Token or credentials.")
        except ObjectDoesNotExist:
            raise serializers.ValidationError("Invalid Token or credentials.")
        return super().validate(attrs)


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=100)

    def validate(self, attrs):
        if (
            attrs.get("email")
            and User.objects.filter(email=attrs.get("email")).exists()
        ):
            raise serializers.ValidationError("Email already exists")
        elif (
            attrs.get("username")
            and User.objects.filter(username=attrs.get("username")).exists()
        ):
            raise serializers.ValidationError("Username already exists")
        return super().validate(attrs)

    class Meta:
        exclude = ["password"]


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ["color_name"]


class PersonSerializer(serializers.ModelSerializer):
    color = ColorSerializer()

    def validate(self, attrs):
        special_chars_str = "!@#$%^&*()_+-=[]{};':\",./<>?"
        if attrs.get("age") and attrs.get("age") < 10:
            raise serializers.ValidationError("Age must be greater than 10")
        elif attrs.get("name") and any(
            c in special_chars_str for c in attrs.get("name")
        ):
            raise serializers.ValidationError("Name cannot contain special characters")
        return super().validate(attrs)

    def create(self, validated_data):
        try:
            color_obj = Color.objects.get(color_name=validated_data.get("color"))
        except ObjectDoesNotExist:
            color_obj = Color.objects.get(id=1)
        validated_data["color"] = color_obj
        return super().create(validated_data)

    def update(self, instance, validated_data):
        color_data = validated_data.pop("color", None)
        if color_data:
            color_name = color_data.get("color_name")
            color, _ = Color.objects.get_or_create(color_name=color_name)
            instance.color = color
        return super().update(instance, validated_data)

    class Meta:
        model = Person
        fields = "__all__"
        # depth = 1
