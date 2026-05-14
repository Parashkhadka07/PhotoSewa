from django.shortcuts import render
from django.contrib import messages
from .forms import PackageForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Package
# Create your views here.

@login_required
def package_list(request):
    # Fetch only packages belonging to the logged-in user
    if(request.user.user_role == "photographer"):
        packages = Package.objects.filter(photographer=request.user.profile)
        return render(request, 'packages/package_list.html', {'packages': packages})
    else:
        messages.error(request,"Do not found any page!")
        return redirect("profile_page")

@login_required
def create_package(request):
    if request.method == "POST":
        form = PackageForm(request.POST)
        if form.is_valid():
            package = form.save(commit=False)
            package.photographer = request.user.profile
            package.save()
            # messages(request,"pakage created sucessfully")
            return redirect('package_list')
    else:
        form = PackageForm()
    return render(request, 'packages/package_form.html', {'form': form})

@login_required
def delete_package(request):
    # 1. Fetch the record
    try:
        
        obj = Package.objects.get(name=request.GET.get("name"),photographer=request.GET.get("photographer"))
        obj.delete()
        messages.success(request,"Package deleted sucessfully")
        return redirect('package_list')
    except Exception as e:
        print("*******",e,"*********")
        messages.error(request,"package not found!!")
        return redirect('package_list')
    