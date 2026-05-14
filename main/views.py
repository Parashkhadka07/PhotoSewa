from django.shortcuts import render
from accounts.models import MyUser
from packages.models import Package


# Create your views here.
def home(request):
    query = request.GET.get('category')
    
    photographers=MyUser.objects.filter(user_role='photographer',profile__kyc_verified="verified")
    if query:
        photographers = photographers.filter(
            profile__specialization=query
        )
    packages=Package.objects.all()
    context={"photographers":photographers,"packages":packages}
    return render(request,"main/home.html",context)


