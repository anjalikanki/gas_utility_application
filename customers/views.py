from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from .models import CustomUser, ServiceRequest
from .forms import CustomerForm, ServiceRequestForm
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm  

def is_admin(user):
    return user.is_superuser

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
            return redirect('login')  
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def home(request):
    return render(request, 'base_generic.html')

@login_required
def view_profile(request):
    return render(request, 'customers/profile.html', {'customer': request.user})

@login_required
def edit_profile(request):
    customer = request.user  
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'customers/edit_profile.html', {'form': form})

@user_passes_test(is_admin)
def list_customers(request):
    customers = CustomUser.objects.all()
    return render(request, 'customers/list_customers.html', {'customers': customers})

@login_required
def create_request(request):
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST, request.FILES)
        if form.is_valid():
            service_request = form.save(commit=False)
            service_request.customer = request.user
            service_request.status = 'pending'  
            service_request.save()
            return redirect('track_requests') 
    else:
        form = ServiceRequestForm()
    return render(request, 'service_requests/create_request.html', {'form': form})

@login_required
def track_requests(request):
    requests = ServiceRequest.objects.filter(customer=request.user)
    return render(request, 'service_requests/track_requests.html', {'requests': requests})


@login_required
def list_requests(request):
    if request.user.is_superuser:       
        requests = ServiceRequest.objects.all()
    else:
        requests = ServiceRequest.objects.filter(customer=request.user)
    return render(request, 'service_requests/list_requests.html', {'requests': requests})


@login_required
def edit_request(request, pk):
    service_request = get_object_or_404(ServiceRequest, pk=pk)
    if request.user != service_request.customer and not request.user.is_superuser:
        return redirect('track_requests')

    if request.method == 'POST':
        form = ServiceRequestForm(request.POST, request.FILES, instance=service_request)

        if form.is_valid():
            service_request = form.save(commit=False)           
            if request.user.is_superuser:
                service_request.status = request.POST.get('status', service_request.status)

            service_request.save()
            return redirect('list_requests') 
    else:
        form = ServiceRequestForm(instance=service_request)

    return render(request, 'service_requests/edit_request.html', {
        'form': form,
        'service_request': service_request,
        'is_admin': request.user.is_superuser 
    })


@user_passes_test(is_admin)
def resolve_request(request, pk):
    service_request = get_object_or_404(ServiceRequest, pk=pk)
    if request.user.is_staff:
        service_request.status = 'resolved'
        service_request.save()
        return redirect('list_requests')  
    else:
        return redirect('track_requests')