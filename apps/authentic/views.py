from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from .forms import createUserForm


def registerPage(request):
    form = createUserForm()

    if request.method == "POST":
        form = createUserForm(request.POST)
        if form.is_valid:
            form.save()
            user = form.cleaned_data.get("username")
            messages.success(request, "Account was successfully created for " + user)

            return redirect("auth:login")

    context = {"form": form}

    return render(request, "authentic/register.html", context)


def loginPage(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("shop:home")

    context = {}
    return render(request, "authentic/login.html", context)


class CustomLoginView(LoginView):
    template_name = "authentic/login.html"
    fields = "__all__"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("shop:home")


def logoutPage(request):
    pass
