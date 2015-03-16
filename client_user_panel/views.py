from django.shortcuts import render, redirect
from admin_user_panel.models import AdminUser
from client_user_panel.models import ClientUser, Client
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# Create your views here.


@login_required(login_url='/login/')
def add_client_info(request):
    user = request.session['user']
    post_data = request.POST
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
                client_name = post_data['client_name']
                client_address = post_data['address']
                if Client.objects.filter(ClientName__exact=client_name).exists():
                    display = render(request, 'add_client.html',
                                     {'wrong': True,
                                      'text': 'There is another Client with the same name. Please Change the name.',
                                      'admin': admin,
                                      'admin_admin': admin_admin})
                else:

                    if AdminUser.objects.filter(username__exact=post_data['username']).exists() or \
                            ClientUser.objects.filter(username__exact=post_data['username']).exists():
                        display = render(request, 'add_client.html',
                                         {'wrong': True,
                                          'text': 'Username already taken. Please try with a different username.',
                                          'admin': admin,
                                          'admin_admin': admin_admin})
                    else:
                        if post_data['re-password'] == post_data['password']:
                            new_client = Client(ClientName=client_name,
                                                Address=client_address)
                            new_client.save()
                            new_client_admin_username = post_data['username']
                            new_client_admin_name = post_data['name']
                            new_client_admin_phone = post_data['phone']
                            new_client_admin_email = post_data['email']
                            new_client_admin_super_admin = True
                            new_client_admin_password = post_data['password']
                            new_client_admin_admin = ClientUser(Client=new_client,
                                                                username=new_client_admin_username,
                                                                Name=new_client_admin_name,
                                                                Email=new_client_admin_email,
                                                                Admin=new_client_admin_super_admin,
                                                                Phone=new_client_admin_phone)
                            new_client_admin_admin.save()
                            new_user = User.objects.create_user(new_client_admin_username,
                                                                new_client_admin_email,
                                                                new_client_admin_password)
                            new_user.save()
                            display = render(request, 'add_client.html',
                                             {'wrong': True,
                                              'text': 'The new user is added successfully',
                                              'admin': admin,
                                              'admin_admin': admin_admin})
                        else:
                            display = render(request, 'add_client.html',
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


def client_modification(request):
    if 'user' in request.session:
        user = request.session['user']
        get_data = request.GET
        # if admin
        if AdminUser.objects.filter(username__exact=user).exists():

            admin = True
            admin_user = AdminUser.objects.get(username__exact=user)
            if admin_user.Active:
                username = get_data['username']
                action = get_data['action']
                selected_user = Client.objects.get(ClientName__exact=username)
                if action == '1':
                    selected_user.Active = True
                    selected_user.save()
                elif action == '2':
                    selected_user.Active = False
                    selected_user.save()
                all_client_users = Client.objects.all()

                display = render(request, 'client_list.html',
                                 {'wrong': True,
                                  'text': 'Success',
                                  'admin': admin,
                                  'all_client_users': all_client_users})
            else:
                logout(request)
                display = render(request, 'login.html',
                                 {'wrong': True,
                                  'text': 'You are not authorized to login.'
                                          ' Please contact administrator for more details'})
        else:
            display = redirect('/')
    else:
        display = redirect('/login')
    return display


def client_user_modification(request):
    if 'user' in request.session:
        user = request.session['user']
        get_data = request.GET
        # if admin
        if ClientUser.objects.filter(username__exact=user).exists():
            client_user = ClientUser.objects.get(username__exact=user)
            client = True
            client_admin = client_user.Admin
            admin_user = ClientUser.objects.get(username__exact=user)
            client_object = client_user.Client
            all_users_of_client = ClientUser.objects.filter(Client=client_object)
            if admin_user.Active:
                username = get_data['username']
                action = get_data['action']
                selected_user = ClientUser.objects.get(username__exact=username)
                if action == '1':
                    selected_user.Active = True
                    selected_user.save()
                elif action == '2':
                    selected_user.Active = False
                    selected_user.save()
                elif action == '3':
                    selected_user.Admin = True
                    selected_user.save()
                elif action == '4':
                    selected_user.Admin = False
                    selected_user.save()
                all_client_users = Client.objects.all()

                display = render(request, 'client_user_list.html',
                                 {'wrong': True,
                                  'text': 'Success',
                                  'all_client_users': all_client_users,
                                  'all_client': all_users_of_client,
                                  'client': client,
                                  'client_admin': client_admin})
            else:
                logout(request)
                display = render(request, 'login.html',
                                 {'wrong': True,
                                  'text': 'You are not authorized to login.'
                                          ' Please contact administrator for more details'})
        else:
            display = redirect('/')
    else:
        display = redirect('/login')
    return display


def transaction(request):
    if 'user' in request.session:
        user = request.session['user']
        get_data = request.GET
        # if admin
        if ClientUser.objects.filter(username__exact=user).exists():
            client_user = ClientUser.objects.get(username__exact=user)
            client = True
            client_admin = client_user.Admin
            admin_user = ClientUser.objects.get(username__exact=user)
            client_object = client_user.Client
            all_users_of_client = ClientUser.objects.filter(Client=client_object)
            if admin_user.Active:
                username = get_data['username']
                action = get_data['action']
                selected_user = ClientUser.objects.get(username__exact=username)
                if action == '1':
                    selected_user.Active = True
                    selected_user.save()
                elif action == '2':
                    selected_user.Active = False
                    selected_user.save()
                elif action == '3':
                    selected_user.Admin = True
                    selected_user.save()
                elif action == '4':
                    selected_user.Admin = False
                    selected_user.save()
                all_client_users = Client.objects.all()

                display = render(request, 'client_user_list.html',
                                 {'wrong': True,
                                  'text': 'Success',
                                  'all_client_users': all_client_users,
                                  'all_client': all_users_of_client,
                                  'client': client,
                                  'client_admin': client_admin})
            else:
                logout(request)
                display = render(request, 'login.html',
                                 {'wrong': True,
                                  'text': 'You are not authorized to login.'
                                          ' Please contact administrator for more details'})
        else:
            display = redirect('/')
    else:
        display = redirect('/login')
    return display


