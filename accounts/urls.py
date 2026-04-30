from django.urls import path
from accounts import views

urlpatterns=[
    path("register/",views.register,name="registration_page"),
    path("login/",views.login,name="login_page"),

]