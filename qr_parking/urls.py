"""
URL configuration for qr_parking project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.urls import path
from parking_app import views

# to correctly import the view from parking_app.views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', views.home, name='home'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    
    # Authentication
    path('register/', views.register, name='register'),
    path('register_view/', views.register_view, name='register_view'),
    path('login/', views.login_view, name='login'),
    
     # Dashboardss
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('admin_dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    

    path('manage_parking_areas/', views.manage_parking_areas, name='manage_parking_areas'),
    path('add_parking_area/', views.add_parking_area, name='add_parking_area'),
    path('edit_parking_area/', views.edit_parking_area, name='edit_parking_area'),
    path('delete_parking_area/<int:area_id>/', views.delete_parking_area, name='delete_parking_area'),
    path('manage_slots/', views.manage_slots, name='manage_slots'),
    path('view_bookings/', views.view_bookings, name='view_bookings'),
    path('manage_parking_areas/', views.manage_parking_areas, name='manage_parking_areas'),
    path('book-slot/', views.book_slot, name='book_slot'),
    path('update_slot_status/<int:slot_id>/', views.update_slot_status, name='update_slot_status'),
    path('cancel_booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),


    path('', include('parking_app.urls')),  # Include app URLs properly

]
