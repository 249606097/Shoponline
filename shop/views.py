from django.shortcuts import render
from .forms import *


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            return render(request, "Welcome.html")
        return render(request, "RegisterPage.html", {"form": form})
    else:
        form = RegisterForm()
        return render(request, "RegisterPage.html", {"form": form})
