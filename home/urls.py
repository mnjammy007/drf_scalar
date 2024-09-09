from django.urls import path, include

from rest_framework.routers import DefaultRouter

from home.views import IndexView, LoginView, PersonViewSet, RegisterView, LogoutView


router = DefaultRouter()
# Use this for ModelViewSet, but for APIView like register, have a look at the code below
router.register("person", PersonViewSet, basename="aadmi")

urlpatterns = [
    path("index/", IndexView.as_view(), name="index"),
    # path("person/", PersonView.as_view(), name="person"),
    path("", include(router.urls)),
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
