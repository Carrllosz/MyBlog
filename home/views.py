from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .form import UserRegisterForm
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context


from .form import *
from django.contrib.auth import logout


def logout_view(request):
    logout(request)
    return redirect('/')

def home(request):
    context = {'blogs' : BlogModel.objects.all()}
    return render(request, 'home.html', context)

#def login_view(request):
#   return render(request, 'login.html')

def Login(request):
    if request.method == 'POST':
        # Authentication Form can also be used
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            form = login(request, user)
            messages.success(request, f'welcome {username}!! ')
            return redirect('home')
        else:
            messages.info(request, f'account do not exist pls sign in')
    
    form = AuthenticationForm()
    return render(request, 'login.html', {'form' : form, 'title' : 'log in'})

#def register_view(request):
#    return render(request, 'register.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            #mail system
            htmly = get_template('Email.html')
            d = {'username' : username}
            subject, from_email, to = 'welcome', 'your_email@gmail.com', email
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, html_content, from_email,[to])
            msg.attach_alternative(html_content, 'html')
            msg.send()
            
            messages.sucess(request, f'yout account has been create! You are now able to log in!')
            return redirect('Login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form, 'title': 'register here'})

def add_blog(request):
    context = {'form': BlogForm}
    try:
        if request.method == 'POST':
            form = BlogForm(request.POST)
            print(request.FILES)
            image = request.FILES['image']
            title = request.POST.get('title')
            user = request.user

            if form.is_valid():
                content = form.cleaned_data['content']
            
            blog_obj =  BlogModel.objects.create(
                user = user, title = title, 
                content = content, image = image
            )
            print(blog_obj)
            return redirect('/add-blog/')
    
    except Exception as e:
        print(e)

    return render(request, 'add_blog.html', context)

def detail_blog(request, slug):
    context = {}
    try:
        blog_obj = BlogModel.objects.filter(slug = slug).first()
        context['blog_obj'] = blog_obj
    except Exception as e:
        print(e)

    return render(request, 'detail_blog.html', context)
    
def see_blog(request):
    context = {}

    try:
        blog_objs = BlogModel.objects.filter(user = request.user)
        context['blog_objs'] = blog_objs
    except Exception as e:
        print(e)

    print(context)
    return render(request, 'see_blog.html', context)

def blog_update(request, slug):
    context = {}
    try:

        blog_obj = BlogModel.objects.get(slug = slug)

        if blog_obj.user != request.user:
            return redirect('/')

        initial_dict = {'context' : blog_obj.content}
        form = BlogForm(initial = initial_dict)
        
        if request.method == 'POST':
            form = BlogForm(request.POST)
            print(request.FILES)
            image = request.FILES['image']
            title = request.POST.get('title')
            user = request.user

            if form.is_valid():
                content = form.cleaned_data['content']

            blog_obj = BlogModel.objects.create(
                user = user, title = title,
                image = image, content = content
            )

        context['blog_obj'] = blog_obj
        context['form'] = form

    except Exception as e:
        print(e)

    return render(request, 'update_blog.html', context)

def blog_delete(request, id):
    try:
        blog_obj = BlogModel.objects.get(id = id)

        if blog_obj.user == request.user:
            blog_obj.delete()

    except Exception as e:
        print(e)

    return redirect('/see-blog/')
    
'''
def verify(request, token):
    try:
        profile_obj = Profile.objects.filter(token = token).first()

        if profile_obj:
            profile_obj.is_varified = True
            profile_obj.save()
        return redirect('/login/')

    except Exception as e:
        print(e)

    return redirect('/')
'''