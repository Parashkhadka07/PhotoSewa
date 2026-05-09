from django.shortcuts import render
from accounts.models import MyUser
# Create your views here.
def home(request):
    photographers=MyUser.objects.filter(user_role='photographer',profile__kyc_verified="verified")
    context={"photographers":photographers}
    return render(request,"main/home.html",context)