from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from admin_user_panel.models import AdminUser
from client_user_panel.models import Client, ClientUser
# Create your views here.


@csrf_exempt
def login_page(request):
    return render(request, 'login.html')


@csrf_exempt
def login_auth(request):
    postdata = request.POST
    print(postdata)
    if 'username' and 'password' in postdata:
        print(postdata['username'])
        print(postdata['password'])
        user = authenticate(username=postdata['username'], password=postdata['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                request.session['user'] = postdata['username']
                if user.is_superuser:
                    res = redirect('/admin')
                else:
                    res = redirect('/')
            else:
                res = render(request, 'login.html',
                             {'wrong': True,
                              'text': 'The password is valid, but the account has been disabled!'})
        else:
            res = render(request, 'login.html',
                         {'wrong': True,
                          'text': 'The username and password you have entered is not correct. Please retry'})
    else:
        res = render(request, 'login.html', {'wrong': False})

    res['Access-Control-Allow-Origin'] = "*"
    res['Access-Control-Allow-Headers'] = "Origin, X-Requested-With, Content-Type, Accept"
    res['Access-Control-Allow-Methods'] = "PUT, GET, POST, DELETE, OPTIONS"
    return res


def logout_now(request):
    logout(request)
    return redirect('/login')


@login_required(login_url='/login/')
def home(request):
    user = request.session['user']
    if not AdminUser.objects.exists():
        print(request.session['user'])
        new_admin = AdminUser(username=user, Name=user, Email=user+'@inflack.com', Admin=True)
        new_admin.save()
    # if admin
    if AdminUser.objects.filter(username__exact=user).exists():
        admin = True
        admin_user = AdminUser.objects.get(username__exact=user)
        admin_admin = admin_user.Admin
        if admin_user.Active:
            display = render(request, 'dashboard.html', {'admin': admin,
                                                         'admin_admin': admin_admin})
        else:
            logout(request)
            display = render(request, 'login.html',
                             {'wrong': True,
                              'text': 'You are not authorized to login. Please contact administrator for more details'})
    # if client
    elif ClientUser.objects.filter(username__exact=user).exists():
        client = True
        client_user = ClientUser.objects.get(username__exact=user)
        client_admin = client_user.Admin
        if client_user.Active:
            display = render(request, 'dashboard.html', {'client': client,
                                                         'client_admin': client_admin})
        else:
            logout(request)
            display = render(request, 'login.html',
                             {'wrong': True,
                              'text': 'You are not authorized to login. Please contact administrator for more details'})
    else:
        logout(request)
        display = render(request, 'login.html',
                         {'wrong': True,
                          'text': 'Something went wrong. Please LOGIN again.'})
    return display


@login_required(login_url='/login/')
def add_admin(request):
    user = request.session['user']
    if not AdminUser.objects.exists():
        print(request.session['user'])
        new_admin = AdminUser(username=user, Name=user, Email=user+'@inflack.com', Admin=True)
        new_admin.save()
    # if admin
    if AdminUser.objects.filter(username__exact=user).exists():
        admin = True
        admin_user = AdminUser.objects.get(username__exact=user)
        admin_admin = admin_user.Admin
        if admin_user.Active:
            if admin_admin:
                display = render(request, 'add_admin.html', {'admin': admin,
                                                             'admin_admin': admin_admin})
            else:
                display = render(request, 'access_denied.html', {'admin': admin,
                                                                 'admin_admin': admin_admin})
        else:
            logout(request)
            display = render(request, 'login.html',
                             {'wrong': True,
                              'text': 'You are not authorized to login. Please contact administrator for more details'})
    else:
        display = redirect('/')
    return display



