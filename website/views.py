from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record

# Create your views here.
def home(request):
    records = Record.objects.all()
    return render(request, 'home.html',{'records':records})

def login_user(request):
    records = Record.objects.all()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have been loged in Successfully')
            return redirect(home)
        else:
            messages.info(request, 'Seems that either username or password is incorrect, Try  again')
            return redirect('login_user')
    else:    
        return render(request, 'login.html', {'records':records})

def logout_user(request):
    logout(request)
    messages.info(request, "You have been logged out..")
    return redirect('login_user')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password='password')
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.SUCCESS(request, "You have Successfully registered! Welcome!")
            return redirect('home')
        else:
            form = SignUpForm()
            return render(request, 'register_user.html', {'form':form})
        
    return render(request, 'register_user.html', {})

def customer_record(request, pk):
    if request.user.is_authenticated:

        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record':customer_record})
    else:
        messages.info(request, "You must need to logged in to view.")
        return redirect('login_user')
    
def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.info(request, "Record deleted succsfully..")
        return redirect('home')
    else:
        messages.info(request, "You must be looged in..")
        return redirect('login_user')
    
def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_record = form.save()
                messages.info(request, "Record Added")
                return redirect('home')
        return render(request, 'add_record.html', {'form':form})
    else:
        messages.info(request, "You must be logged in..")
        return redirect('login_user')
