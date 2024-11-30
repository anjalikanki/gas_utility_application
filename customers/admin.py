from django.contrib import admin
from .models import CustomUser,ServiceRequest

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone', 'address')  
    readonly_fields = ('date_joined', 'last_login')  
    list_filter = ('date_joined',)  
    date_hierarchy = 'date_joined' 

class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'request_type', 'customer', 'status', 'created_at'] 
    readonly_fields = ['created_at']  
    list_filter = ['status', 'created_at'] 
    search_fields = ['customer__username', 'request_type']  

admin.site.register(CustomUser, CustomerAdmin)
admin.site.register(ServiceRequest, ServiceRequestAdmin)