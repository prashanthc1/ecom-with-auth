from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import createUserForm


def registerPage(request):
    form = createUserForm()

    if request.method == "POST":
        form = createUserForm(request.POST)
        if form.is_valid:
            form.save()
            user = form.cleaned_data.get("username")
            messages.success(request, "Account was successfully created for " + user)

            return redirect("login")

    context = {"form": form}

    return render(request, "authentic/register.html", context)


def loginPage(request):
    return render(request, "authentic/login.html")
