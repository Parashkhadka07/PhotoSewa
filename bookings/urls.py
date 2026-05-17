from django.urls import path
from bookings import views


urlpatterns=[
  # booking/urls.py
     path('book/<int:pkg_id>/', views.book_package, name='book_package'), 
     path('my-bookings/', views.my_bookings, name='my_bookings'),
     path('booking/<int:booking_id>/<str:action>/', views.update_booking_status, name='update_booking_status'),
]