from django.shortcuts import render
from accounts.models import MyUser
# Create your views here.
def home(request):
    query = request.GET.get('category')
    
    photographers=MyUser.objects.filter(user_role='photographer',profile__kyc_verified="verified")
    if query:
        photographers = photographers.filter(
            profile__specialization=query
        )
    context={"photographers":photographers}
    return render(request,"main/home.html",context)