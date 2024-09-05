from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view
from rest_framework.response import Response

from home.models import Person
from home.serializers import PersonSerializer, LoginSerializer


@api_view(["GET"])
def index(request):
    courses = {
        "course_name": "python",
        "topics": ["django", "flask", "fastapi"],
        "course_provider": "scalar",
    }
    return Response(courses)


@api_view(["POST"])
def login(request):
    data = request.data
    serializer = LoginSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    return Response(serializer.data)


@api_view(["GET", "POST", "PUT", "PATCH", "DELETE"])
def people(request):
    if request.method == "GET":
        people = Person.objects.filter(color__isnull=False)
        serializer = PersonSerializer(people, many=True)
    elif request.method == "POST":
        data = request.data
        serializer = PersonSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
    elif request.method == "PUT":
        data = request.data
        person = get_object_or_404(Person, id=data.get("id"))
        serializer = PersonSerializer(person, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
    elif request.method == "PATCH":
        data = request.data
        person = get_object_or_404(Person, id=data.get("id"))
        serializer = PersonSerializer(person, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
    else:
        data = request.data
        person = get_object_or_404(Person, id=data.get("id"))
        person.delete()
        return Response({"message": "Person deleted"})

    return Response(serializer.data)
