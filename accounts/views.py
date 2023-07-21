from django.contrib.auth.models import Group
from django.contrib.auth import authenticate,login
from django.shortcuts import render, redirect
from accounts.forms import RegistrationForm, LoginForm


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.subscription_type = request.POST.get('subscription_type')
            user.save()

            group_name = user.subscription_type
            if group_name == 'streamer':
                group = Group.objects.get(name='streamer')
            elif group_name == 'viewer':
                group = Group.objects.get(name='viewer')
            else:
                group = None

            if group:
                user.groups.add(group)

    #         Authenticate and Login the user
            authenticated_user = authenticate(request, email=user.email, password=form.cleaned_data['password1'])
            if authenticated_user:
                login(request, authenticated_user)
                return redirect('index')
    else:
        form = RegistrationForm()

    return render(request, 'accounts/registration.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                form.add_error(None, 'Invalid Email or Password ')
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})
