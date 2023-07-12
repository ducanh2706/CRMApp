from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.urls import reverse
from .forms import SignUpForm, ChangePasswordForm, AddRecordForm
from .models import Record
# Create your views here.



def home(request):

    records = Record.objects.all()

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate
        user = authenticate(request, username=username,password=password)
        print(username, password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in")
            return HttpResponseRedirect(reverse('mysite:home'))
        else:
            messages.warning(request, "There was an error logging in. Please try again!")
            return HttpResponseRedirect(reverse('mysite:home'))

    else:
        return render(request, 'mysite/home.html', {'records' : records})

    
def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return HttpResponseRedirect(reverse('mysite:home'))

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'You have successfully registered')
            return HttpResponseRedirect(reverse('mysite:home'))
    else:
        form = SignUpForm()
        return render(request, 'mysite/register.html', {'form': form})

def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password is updated successfully')
            return HttpResponseRedirect(reverse('mysite:home'))
        else:
            messages.warning(request, 'Please correct the error')

    else:
        form = ChangePasswordForm(request.user)

    return render(request, 'mysite/change_password.html', {'form': form})

def view_record(request, pk):
    if not request.user.is_authenticated:
        messages.warning(request, 'You have to log in before having access to that page')
        return HttpResponseRedirect(reverse('mysite:home'))
    else:
        try:
            record = Record.objects.get(pk=pk)
        except Record.DoesNotExist:
            raise Http404("Record Not Found")
        return render(request, 'mysite/record.html', {'customer_record': record})
        
def add_record(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'You have to log in before having access to that page')
        return HttpResponseRedirect(reverse('mysite:home'))
    else:
        if request.method == 'POST':
            form = AddRecordForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Record added...')
                return HttpResponseRedirect(reverse('mysite:home'))

        form = AddRecordForm()
        return render(request, 'mysite/add_record.html', {'form': form})

def delete_record(request, pk):
    if not request.user.is_authenticated:
        messages.warning(request, 'You have to log in before having access to that page')
        return HttpResponseRedirect(reverse('mysite:home'))
    else:
        try:
            record = Record.objects.get(pk=pk)
        except Record.DoesNotExist:
            raise Http404("Record Not Found")
        
        record.delete()
        messages.success(request, 'Record Deleted Successfully')
        return HttpResponseRedirect(reverse('mysite:home'))

def update_record(request, pk):
    if not request.user.is_authenticated:
        messages.warning(request, 'You have to log in before having access to that page')
        return HttpResponseRedirect(reverse('mysite:home'))
    else:
        try:
            record = Record.objects.get(pk=pk)
        except Record.DoesNotExist:
            raise Http404('Record Not Found')

        if request.method == 'POST':
            form = AddRecordForm(request.POST, instance=record)
            if form.is_valid():
                form.save()
                messages.success(request, 'Record Has Been Updated')
                return HttpResponseRedirect(reverse('mysite:view_record', args=(pk, )))
        else:
            form = AddRecordForm(instance=record)
            return render(request, 'mysite/update_record.html', {'form': form})


