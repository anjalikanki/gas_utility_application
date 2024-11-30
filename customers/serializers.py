from rest_framework import serializers
from .models import Customer, ServiceRequest


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'address', 'phone_number', 'email', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class ServiceRequestSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    
    class Meta:
        model = ServiceRequest
        fields = ['id', 'customer', 'request_type', 'description', 'status', 'created_at', 'resolved_at']
        read_only_fields = ['created_at', 'resolved_at']
    
    def create(self, validated_data):
        customer_data = validated_data.pop('customer', None)
        service_request = ServiceRequest.objects.create(**validated_data)
        if customer_data:
            customer = Customer.objects.create(**customer_data)
            service_request.customer = customer
            service_request.save()
        
        return service_request


class ServiceRequestUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRequest
        fields = ['id', 'request_type', 'description', 'status', 'resolved_at']
        read_only_fields = ['id', 'created_at']
    def validate_status(self, value):
        if value not in ['Pending', 'Resolved', 'In Progress']:
            raise serializers.ValidationError("Status must be one of: Pending, Resolved, In Progress.")
        return value


class ServiceRequestResolveSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRequest
        fields = ['id', 'status', 'resolved_at']
        read_only_fields = ['id', 'created_at']
    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        if instance.status == 'Resolved' and not instance.resolved_at:
            instance.resolved_at = validated_data.get('resolved_at', timezone.now())
        instance.save()
        return instance