from django.shortcuts import render, redirect
from admin_user_panel.models import AdminUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
# Create your views here.


@login_required(login_url='/login/')
def add_admin_info(request):
    user = request.session['user']
    post_data = request.POST
    # print(post_data['super-admin'])
    if not AdminUser.objects.exists():
        print(request.session['user'])
        new_admin = AdminUser(username=user, Name=user, Email=user+'@inflack.com', Admin=True)
        new_admin.save()
    if 'username' in post_data and 'csrfmiddlewaretoken' in post_data:
        # if admin
        if AdminUser.objects.filter(username__exact=user).exists():
            admin = True
            admin_user = AdminUser.objects.get(username__exact=user)
            admin_admin = admin_user.Admin
            if admin_user.Active and admin_admin:
                if AdminUser.objects.filter(username__exact=post_data['username']).exists():
                    display = render(request, 'add_admin.html',
                                     {'wrong': True,
                                      'text': 'Username already taken. Please try with a different username.',
                                      'admin': admin,
                                      'admin_admin': admin_admin})
                else:
                    if post_data['re-password'] == post_data['password']:
                        new_admin_username = post_data['username']
                        new_admin_name = post_data['name']
                        new_admin_phone = post_data['phone']
                        new_admin_email = post_data['email']
                        if 'super-admin' in post_data and post_data['super-admin'] == 'on':
                            new_admin_super_admin = True
                        else:
                            new_admin_super_admin = False
                        new_admin_password = post_data['password']
                        new_added_admin = AdminUser(username=new_admin_username,
                                                    Name=new_admin_name,
                                                    Email=new_admin_email,
                                                    Admin=new_admin_super_admin,
                                                    Phone=new_admin_phone)
                        new_added_admin.save()
                        new_user = User.objects.create_user(new_admin_username,
                                                            new_admin_email,
                                                            new_admin_password)
                        new_user.save()
                        display = render(request, 'add_admin.html',
                                         {'wrong': True,
                                          'text': 'The new user is added successfully',
                                          'admin': admin,
                                          'admin_admin': admin_admin})
                    else:
                        display = render(request, 'add_admin.html',
                                         {'wrong': True,
                                          'text': 'Passwords do not match. Please Try Again.',
                                          'admin': admin,
                                          'admin_admin': admin_admin})
            else:
                logout(request)
                display = render(request, 'login.html',
                                 {'wrong': True,
                                  'text': 'You are not authorized to login.'
                                          ' Please contact administrator for more details'})
        else:
            display = redirect('/')
    else:
        display = redirect('/add_admin/')
    return display


@login_required(login_url='/login/')
def admin_list(request):
    user = request.session['user']
    post_data = request.POST
    # if admin
    if AdminUser.objects.filter(username__exact=user).exists():
        admin = True
        admin_user = AdminUser.objects.get(username__exact=user)
        admin_admin = admin_user.Admin
        if admin_user.Active and admin_admin:
            all_admin_users = AdminUser.objects.all()
            display = render(request, 'admin_list.html',
                             {'wrong': True,
                              'text': 'Passwords do not match. Please Try Again.',
                              'admin': admin,
                              'admin_admin': admin_admin,
                              'all_admin_users': all_admin_users})
        else:
            logout(request)
            display = render(request, 'login.html',
                             {'wrong': True,
                              'text': 'You are not authorized to login.'
                                      ' Please contact administrator for more details'})
    else:
        display = redirect('/')
    return display