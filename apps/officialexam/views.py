from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
    if 'authenticator' not in request.session:
        return render(request, 'officialexam/index.html')
    else:
        return redirect('/wishes')

def wishes(request):
    if 'authenticator' not in request.session:
        return render(request, 'officialexam/hacker.html')
    else:
        context = {
            'user': User.objects.get(email_hash=request.session['authenticator']),
            'wishes': User.objects.get(email_hash=request.session['authenticator']).wishes.all(),
            'granted_wishes': Granted_wish.objects.all()
        }
        return render(request, 'officialexam/wishes.html', context)

def hacker(request):
    return render(request, 'officialexam/hacker.html')

def new(request):
    if 'authenticator' not in request.session:
        return render(request, 'officialexam/hacker.html')
    else:
        context = {
            'user': User.objects.get(email_hash=request.session['authenticator'])
        }
        return render(request, 'officialexam/new.html', context)

def edit(request, id):
    if 'authenticator' not in request.session:
        return render(request, 'officialexam/hacker.html')
    else:
        context = {
            'user': User.objects.get(email_hash=request.session['authenticator']),
            'wish': Wish.objects.get(id=id)
        }
        return render(request, 'officialexam/edit.html', context)

def stats(request):
    if 'authenticator' not in request.session:
        return render(request, 'officialexam/hacker.html')
    else:
        context = {
            'user': User.objects.get(email_hash=request.session['authenticator']),
            'granted_wishes': Granted_wish.objects.count(),
            'user_granted_wishes': User.objects.get(email_hash=request.session['authenticator']).granted_wishes.count(),
            'user_pending_wishes': User.objects.get(email_hash=request.session['authenticator']).wishes.count()
        }
        return render(request, 'officialexam/stats.html', context)

def register(request):
    if request.method == 'POST':
        errors = User.objects.registration_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags='register')
            return redirect('/')
        else:
            create = User.objects.create_user(request.POST)
            messages.success(request, "User successfully created!")
            user = User.objects.last()
            request.session['authenticator'] = user.email_hash
            request.session['user_id'] = user.id
        return redirect('/wishes')    
    else:
        return redirect('/')

def login(request):
    if request.method == 'POST':
        errors = User.objects.login_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags='login')
            return redirect('/')
        else:
            user = User.objects.get(email = request.POST['email'])
            request.session['authenticator'] = user.email_hash
            request.session['user_id'] = user.id
        return redirect('/wishes')    
    else:
        return redirect('/')

def logout(request):
    if request.method == 'POST':
        request.session.clear()
        return redirect('/')
    else:
        return redirect('/')

def new_wish(request):
    if request.method == 'POST':
        errors = Wish.objects.wish_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/new')
        else:
            Wish.objects.create(item=request.POST['item'], desc=request.POST['desc'], user=User.objects.get(id=request.POST['user_id']))
            return redirect('/wishes')
    else:
        return redirect('/')

def grant(request):
    if request.method == 'POST':
        Granted_wish.objects.create(item=request.POST['wish_item'], user=User.objects.get(id=request.POST['user_id']), date_added=request.POST['wish_created'])
        wish = Wish.objects.get(id=request.POST['wish_id'])
        wish.delete()
        return redirect('/wishes')
    else:
        return redirect('/')

def update(request, id):
    if request.method == 'POST':
        errors = Wish.objects.wish_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
                return redirect('/edit')
        else:
            wish = Wish.objects.get(id= id)
            wish.item = request.POST['item']
            wish.desc = request.POST['desc']
            wish.save()
            return redirect('/wishes')    
    else:
        return redirect('/')

def like(request):
    if request.method == 'POST':
        granted = Granted_wish.objects.get(id=request.POST['grant_id'])
        user = User.objects.get(id=request.POST['user_id'])
        if granted.user_id == user.id:
            messages.error(request, "Users may not like their own wishes.")
            return redirect('/wishes')
        if len(granted.likes.filter(id=request.POST['user_id'])) > 0:
            messages.error(request, "You have already liked this wish.")
            return redirect('/wishes')
        else:
            granted.likes.add(user)
            return redirect('/wishes')

def delete(request):
    if request.method == 'POST':
        wish = Wish.objects.get(id=request.POST['wish_id'])
        wish.delete()
        return redirect('/wishes')
    else:
        return redirect('/')