from django.urls import path
from packages import views


urlpatterns=[
    path('', views.package_list, name='package_list'),
    path('new/', views.create_package, name='create_package'),
    path("delete",views.delete_package,name="delete_package"),
]