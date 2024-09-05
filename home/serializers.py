from rest_framework import serializers

from .models import Person, Color


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=100)

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ["color_name"]


class PersonSerializer(serializers.ModelSerializer):
    color = ColorSerializer(read_only=True)
    color_info = serializers.SerializerMethodField()

    def get_color_info(self, obj):
        color_obj = Color.objects.get(id=obj.color.id)
        return {"color_name": color_obj.color_name, "hex_code": "#000000"}

    def validate(self, attrs):
        special_chars_str = "!@#$%^&*()_+-=[]{};':\",./<>?"
        if attrs.get("age") < 10:
            raise serializers.ValidationError("Age must be greater than 10")
        elif any(c in special_chars_str for c in attrs.get("name")):
            raise serializers.ValidationError("Name cannot contain special characters")
        return super().validate(attrs)

    class Meta:
        model = Person
        fields = "__all__"
        # depth = 1
