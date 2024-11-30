from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from customers import views as customer_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', customer_views.home, name='home'),
    path('register/', customer_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),  
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('edit-profile/', customer_views.edit_profile, name='edit_profile'),
    path('list_customers/', customer_views.list_customers, name='list_customers'),
    path('create-request/', customer_views.create_request, name='create_request'),
    path('track-requests/', customer_views.track_requests, name='track_requests'),
    path('service-requests/', customer_views.list_requests, name='list_requests'),
    path('service-requests/create/', customer_views.create_request, name='create_request'),
    path('service-requests/<int:pk>/edit/', customer_views.edit_request, name='edit_request'),
    path('service-requests/<int:pk>/resolve/', customer_views.resolve_request, name='resolve_request'),
]