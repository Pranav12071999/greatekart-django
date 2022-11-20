from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
# Account Verification
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.http import HttpResponse
# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = request.POST['password']
            confirm_password = request.POST['confirm_password']
            print(f'password = {password}')
            print(f'confirm_password = {confirm_password}')
            username = email.split('@')[0]
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email = email, username = username)
            user.phone_number = phone_number
            user.save()
            # User activation
            current_site = get_current_site(request)
            mail_subject = "Please activate your account"
            message = render_to_string('accounts/account_verification_email.html', {
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to = [to_email])
            send_email.send()
            messages.success(request, f'We have sent you verification mail on {email}. Please verify by clicking on link.')
            return redirect('http://127.0.0.1:8000/accounts/register/')
    else:
        form = RegistrationForm()
    context = {'form':form}
    return render(request, 'accounts/register.html', context)
    
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        print(f'Login password = {password}')
        user = auth.authenticate(email = email, password = password)
        print(f'User = {user}')

        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid Credentials !!')
            return redirect('login')
    return render(request, 'accounts/login.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out !!')
    return redirect('login')

def activate(request, uidb64, token):
    try:
        #Decoding uid 
       uid = urlsafe_base64_decode(uidb64).decode()
       # Getting user by uid
       user = Account._default_manager.get(pk = uid)

    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    # Checking whether token created and token given is same or not
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        messages.success(request, ' Congratulations !! Your account has been activated successfully !!')
        return redirect('login')
    else:
        messages.error(request, 'Invalid verification link !!') 
        return redirect('register')