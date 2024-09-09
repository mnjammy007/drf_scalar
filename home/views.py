from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.paginator import Paginator

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action

from home.models import Person
from home.serializers import PersonSerializer, LoginSerializer, RegisterSerializer, LogoutSerializer


class IndexView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        courses = {
            "course_name": "python",
            "topics": ["django", "flask", "fastapi"],
            "course_provider": "scalar",
        }
        return Response(courses)


class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            username=serializer.data.get("email"),
            password=serializer.data.get("password"),
        )
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"message": f"Login request for user {serializer.data.get("email")} is successful.", "token":str(token)})
        return Response({"message": "Invalid credentials or User does not exist."}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request.user.auth_token.delete()
        return Response({"message": "Logout successful."})

# class PersonView(APIView):
#     def get(self, request):
#         # people = Person.objects.filter(color__isnull=False)
#         people = Person.objects.all()
#         serializer = PersonSerializer(people, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         data = request.data
#         serializer = PersonSerializer(data=data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

#     def put(self, request):
#         data = request.data
#         person = get_object_or_404(Person, id=data.get("id"))
#         serializer = PersonSerializer(person, data=data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

#     def patch(self, request):
#         data = request.data
#         person = get_object_or_404(Person, id=data.get("id"))
#         serializer = PersonSerializer(person, data=data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

#     def delete(self, request):
#         data = request.data
#         person = get_object_or_404(Person, id=data.get("id"))
#         person.delete()
#         return Response({"message": "Person deleted successfully"})

class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.create(
            **serializer.data
        )
        user.set_password(serializer.data.get("password"))
        user.save()
        if user:
            token, _ = Token.objects.get_or_create(user=user)
        return Response({"message": "User created successfully.", "email":serializer.data.get('email'), "token":str(token)},status=status.HTTP_201_CREATED)
    
class PersonViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = PersonSerializer
    queryset = Person.objects.all()

    def list(self, request):
        page = request.query_params.get("page", 1)
        page_size = 3
        try:
            search_query = request.query_params.get("search")
            if search_query:
                people = self.queryset.filter(name__icontains=search_query)
            else:
                people = Person.objects.all()
            paginator = Paginator(people, page_size)
            # Exception is raised only if we try to access a page that is out of range using paginator.page(page)
            serializer = PersonSerializer(paginator.page(page), many=True)
            # serializer = PersonSerializer(people, many=True)
            if serializer.data:
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response(serializer.data, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response({"message": "Invalid page"})
    
    @action(detail=True, methods=["POST"])
    def send_mail_to_person(self, request,pk):
        # data = request.data
        # serializer = PersonSerializer(data=data,partial=True)
        # serializer.is_valid(raise_exception=True)
        # person = Person.objects.get(id=serializer.data.get("id"))
        # mail_data = {
        #     "subject":"Welcome to our platform",
        #     "message":f"Hello {person.name}, welcome to our platform.",
        #     "from_email":"test@gmail.com",
        #     "recipient_list":[person.email],
        #     "fail_silently":False,
        # }
        return Response({"message": "Mail sent successfully.","mail_data":"mail_data"})
