from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin panel URL
    path('admin/', admin.site.urls),

    # Include URLs from the 'customers' app
    path('customers/', include('customers.urls')),  # Customers app URLs

    # Set customers home page as the default landing page
    path('', include('customers.urls')),  # Redirect to the customer views (e.g., home page)
]
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)