from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from authenticate.models import UserProfile
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.db import IntegrityError


def my_login(request):

    if request.method == 'POST' and 'username' in request.POST and request.POST['username'] != '':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/queue')
            # index(request)
            # return render(request, 'success.html', {'username': request.user.username, 'email': request.user.email})
        else:
            user_message = 'Invalid login'
            return render(request, 'login.html', {'user_message': user_message})
    else:
        return render(request,'login.html', {'user_message': 'Please log in'})


def account_confirmed(request):
    return redirect('/queue')


def create_account(request: object):
    if not request.user.is_authenticated:
        user_message = "Please login to access the Training Management System"
        return render(request, 'login.html', {'user_message': user_message})

    if request.POST.get('cancel'):
        return redirect('/queue')

    if request.method == 'GET':
        return render(request, 'create_account.html', {'user_message': 'message'})
    else:
        try:
            user = User.objects.create_user(request.POST['username'],  request.POST['email'], request.POST['password'])
        except(ValueError):
            return render(request, 'create_account.html', {'user_message': 'Value Error: You must specify a User name','profile_info': UserProfile.objects.get(username=request.user.username)})
        except(IntegrityError):
            return render(request, 'create_account.html', {'user_message': 'Integrity Error: The username is not unique', 'profile_info': UserProfile.objects.get(username=request.user.username)})

        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.save()
        my_profile = UserProfile(username=request.POST['username'], role=request.POST['role'], phone=request.POST['phone'], topic_interest=request.POST['topic_interest'], notes=request.POST['notes'] )
        my_profile.save()
        message = 'A new account has been created for: '
        return render(request, 'account_confirmation.html', {'user_message': message, 'user': user, 'my_profile': my_profile})


def get_profile_data(request):
    profile_info =  UserProfile.objects.filter(username=request.user.username)
    print(request.user.first_name)
    return render(request, 'profile_data.html', {'username': profile_info.values_list('username', flat=True)[0],'first_name': request.user.first_name,'last_name': request.user.last_name, 'email': request.user.email,'role': profile_info.values_list('role', flat=True)[0], 'phone': profile_info.values_list('phone', flat=True)[0], 'topic_interest': profile_info.values_list('topic_interest', flat=True)[0], 'notes': profile_info.values_list('notes', flat=True)[0]})
    # return render(request, 'profile_data.html')


def my_logout(request):
    logout(request)
    return render(request, 'login.html')