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
                            new_client_admin_admin = AdminUser(Client=new_client,
                                                               username=new_client_admin_username,
                                                               Name=new_client_admin_name,
                                                               Email=new_client_admin_email,
                                                               Admin=new_client_admin_super_admin)
                                                               # Phone=new_client_admin_phone)
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
