from django.shortcuts import render,redirect
from .admin import UserCreationForm
from django.contrib import messages

# Create your views here.
def register(request):
    print("***********************",request.POST,"**********************")
    if request.method == "POST":
        submitted_form=UserCreationForm(request.POST)
        
        if submitted_form.is_valid():
            submitted_form.save()
            messages.success(request,"registration sucessful")
            return redirect("home_page")
        else:
            return render(request, "accounts/registration.html", {"form": submitted_form})
    else:
        return render(request, "accounts/registration.html")

        
    

def login(request):
    return render(request,"accounts/login.html")
    