from django.urls import path
from accounts import views

urlpatterns=[
    path("register/",views.register,name="registration_page"),
    path("login/",views.login_view,name="login_page"),
    path("logout/",views.logout_view,name="logout_page"),
    path("profile/",views.profile,name="profile_page"),
    path("kyc/",views.Kyc,name="kyc_page"),
    path("uploads/",views.upload_profile_pic,name="profile_upload"),
    path("delete_profilr",views.remove_profile,name="remove_profile"),
    path("update_profile/",views.edit_profile_photo,name="edit_profile_photo"),
    path("updateprofile_client/",views.profile_client,name="profile_client"),

    


]