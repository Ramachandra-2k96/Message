from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from mymessage.models import ChatMessage
from django.contrib.auth.decorators import login_required
from mymessage.forms import LoginForm, SignUpForm
from django.contrib.auth import login as auth_login, authenticate,logout
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def custom_login1(request):
    login_form = LoginForm()
    signup_form = SignUpForm()
    if request.method == 'POST':
        if 'login-submit' in request.POST:
            form = LoginForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(request, username=email, password=password)
                if user is not None:
                    auth_login(request, user)
                    messages.add_message(request, messages.SUCCESS, 'Login successful!')
                    return redirect('chat_view1', permanent=True)  # 'permanent=True' will cause a 301 redirect  
                else:
                    messages.error(request, 'Invalid username or password')
            else:
                messages.error(request, 'Login form is not valid')
                print(form.errors)
        elif 'signup-submit' in request.POST:
            form = SignUpForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.save()
                auth_login(request, user)
                messages.success(request, 'Signup successful!')
                return redirect('chat_view1')
            else:
                messages.error(request, 'Signup form is not valid')
                print(form.errors)

    return render(request, 'my_message/index.html', {'login_form': login_form, 'signup_form': signup_form})

from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import ChatMessage
@csrf_exempt
@login_required
def chat_view1(request):
    if request.method == 'POST':
        user = request.user
        message_content = request.POST.get('message_input')
        if message_content:
            ChatMessage.objects.create(user=request.user, content=message_content)
            return JsonResponse({'status': 'success'})
    messages = ChatMessage.objects.all()
    return render(request, 'my_message/home.html', {'messages': messages})

@login_required
def get_m(request):
    user = request.user
    messages = ChatMessage.objects.all()
    messages_data = [{'user': message.user.first_name, 'content': message.content,'timestamp': message.timestamp, 'is_mine': message.user == request.user} for message in messages]
    return JsonResponse({'messages': messages_data})