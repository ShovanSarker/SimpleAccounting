from django.shortcuts import render, redirect
from admin_user_panel.models import AdminUser
from client_user_panel.models import ClientUser, Client
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from bank.models import Bank

# Create your views here.


def add_a_bank(request):
    if 'user' in request.session:
        user = request.session['user']
        # if client
        if ClientUser.objects.filter(username__exact=user).exists():
            client_user = ClientUser.objects.get(username__exact=user)
            client = True
            client_admin = client_user.Admin

            admin_user = ClientUser.objects.get(username__exact=user)
            if admin_user.Active:
                if admin_user.Admin:
                    client_object = client_user.Client
                    post_data = request.POST
                    bank_name = post_data['bank_name']
                    bank_account = post_data['bank_account']
                    bank_balance = post_data['bank_balance']
                    new_bank = Bank(ClientName=client_object,
                                    NameOfTheBank=bank_name,
                                    AccountNumber=bank_account,
                                    Balance=bank_balance)
                    new_bank.save()
                    display = redirect('/')
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