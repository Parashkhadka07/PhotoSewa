from django.shortcuts import render,redirect
from .admin import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import Profile
from .forms import KycForm,UpdateForm,UpdateFormClient

# Create your views here.

def login_view(request):
    if request.method=="POST":
        user=authenticate(request, email=request.POST.get("email"),password=request.POST.get("password"))
        if user is not None:
            login(request,user)
            if not request.POST.get("remember_me"):
                request.session.set_expiry(0)
            messages.success(request,"Login Sucessfull !")
            
            return redirect("profile_page")
        else:
            messages.error(request,"User credentials do not match !")
            return redirect("login_page")

    else:   
        return render(request,"accounts/login.html")




def register(request):
    if request.method == "POST":
        submitted_form=UserCreationForm(request.POST)
        
        if submitted_form.is_valid():
            registered_user=submitted_form.save()
            Profile.objects.create(user=registered_user)


            messages.success(request,"Registration Sucessful !")
            return redirect("login_page")
        else:
            return render(request, "accounts/registration.html", {"form": submitted_form})
    else:
        return render(request, "accounts/registration.html")

        
    
def logout_view(request):
    logout(request)
    messages.success(request,"LogOut Sucessfull !")
    return redirect("home_page")
    

#profile
def profile(request):
    return render(request,"accounts/profiles/profile.html")



def upload_profile_pic(request):
    photo = request.FILES['profile_photo'] 
    request.user.profile.profile_photo = photo  # ADD THIS
    request.user.profile.save()  
  
    return redirect("profile_page")



def remove_profile(request):
    request.user.profile.profile_photo = None
    request.user.profile.save() 
    messages.success(request,"profile picture deleted sucessfully!")
    return redirect("profile_page")

#this is for the updating data
def edit_profile_photo(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = UpdateForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('home_page')
        else:
            # This allows the user to see exactly what went wrong
            messages.error(request, "Please fix the errors below.")
    else:
        form = UpdateForm(instance=profile)

    return render(request, "accounts/profiles/edit_profile.html", {"form": form, "profile": profile})


def profile_client(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = UpdateFormClient(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('home_page')
        else:
            # This allows the user to see exactly what went wrong
            messages.error(request, "Please fix the errors below.")
    else:
        form = UpdateFormClient(instance=profile)

    return render(request, "accounts/profiles/edit_profile.html", {"form": form, "profile": profile})

   


def Kyc(request):
    profile,created= Profile.objects.get_or_create(user=request.user)
    print("*********",request.POST,"**********")
    if request.method == 'POST':
        # 2. Feed the HTML data (POST) and Files into the ModelForm
        if profile.kyc_verified in [Profile.KYC_STATUS.VERIFIED, Profile.KYC_STATUS.IN_review]:
            messages.error(request, "Documents cannot be updated while under review or verified.")
            return redirect("kyc_page")
        form = KycForm(request.POST, request.FILES, instance=profile)

        # 3. Validation Trigger
        if form.is_valid():
            
            profile.kyc_verified=profile.KYC_STATUS.IN_review
            # 4. Storage: save() writes to the DB and handles the files automatically
            form.save() 
           
            messages.success(request,"kyc started sucessfully!")
            return redirect('profile_page') 
        else:
           
            print(form.errors) 
    else:
        form = KycForm(instance=profile)

    return render(request, 'accounts/profiles/kyc.html', {'form': form})