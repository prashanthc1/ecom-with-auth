from django.urls import path

from .views import loginPage, registerPage

app_name = "auth"

urlpatterns = [
    path("register/", registerPage, name="register"),
    path("login/", loginPage, name="login"),
]
