from django.urls import path

from .views import CustomLoginView, loginPage, logoutPage, registerPage

app_name = "auth"

urlpatterns = [
    path("register/", registerPage, name="register"),
    # path("login/", loginPage, name="login"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", logoutPage, name="logout"),
]
