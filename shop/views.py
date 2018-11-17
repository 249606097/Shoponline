from django.shortcuts import render
from .forms import *
from .models import *
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


def turn_to_welcome_page(request):
    return render(request, "Welcome.html")


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            password_re = form.cleaned_data["password_re"]
            answer = form.cleaned_data["answer"]
            if password == password_re:
                encrypted_password = make_password(password)
                user_to_save = User(user_name=username, user_password=encrypted_password, user_answer=answer,
                                    user_type="1")
                user_to_save.save()
                return HttpResponseRedirect(reverse('shop:welcome'))
            else:
                return render(request, "RegisterPage.html", {"form": form})
        return render(request, "RegisterPage.html", {"form": form})
    else:
        form = RegisterForm()
        return render(request, "RegisterPage.html", {"form": form})
