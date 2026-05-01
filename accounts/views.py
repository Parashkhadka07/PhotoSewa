from django.shortcuts import render,redirect
from .admin import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout

# Create your views here.

def login_view(request):
    if request.method=="POST":
        user=authenticate(request, email=request.POST.get("email"),password=request.POST.get("password"))
        if user is not None:
            login(request,user)
            if not request.POST.get("remember_me"):
                request.session.set_expiry(0)
            messages.success(request,"Login Sucessfull !")
            return redirect("home_page")
        else:
            messages.error(request,"Email or Password did not match !")
            return redirect("login_page")

    else:   
        return render(request,"accounts/login.html")




def register(request):
    if request.method == "POST":
        submitted_form=UserCreationForm(request.POST)
        
        if submitted_form.is_valid():
            submitted_form.save()
            messages.success(request,"Registration Sucessful !")
            return redirect("login_page")
        else:
            return render(request, "accounts/registration.html", {"form": submitted_form})
    else:
        return render(request, "accounts/registration.html")

        
    
def logout_view(request):
    logout(request)
    return redirect("home_page")
    