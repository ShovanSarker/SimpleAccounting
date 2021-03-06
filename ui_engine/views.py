#!/usr/bin/python

import smtplib
from smtplib import SMTPException
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from admin_user_panel.models import AdminUser
from client_user_panel.models import Client, ClientUser, ClientUserSuggestionNames, ClientUserSuggestionPurpose
from cash.models import Cash
from bank.models import Bank
from django.contrib.auth.models import User
from transaction.models import Transaction, BorrowedTransaction, LentTransaction
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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
    page_title = '|Home|'
    loggedInUser = ''
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
        loggedInUser = admin_user.Name
        if admin_user.Active:
            display = render(request, 'dashboard.html', {'admin': admin,
                                                         'loggedInUser': loggedInUser,
                                                         'page_title': page_title,
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
        loggedInUser = client_user.Name
        client_name = client_user.Client.ClientName
        if client_user.Active:
            client_object = client_user.Client
            banks = Bank.objects.filter(ClientName=client_object, Active=True)
            cash = Cash.objects.get(ClientName=client_object)

            if 'err' in request.GET and request.GET['err'] == '1':
                wrn = True
                text = 'Insufficient Balance'
            else:
                wrn = False
                text = ''
            display = render(request, 'client_dashboard.html', {'client': client,
                                                                'home_active': True,
                                                                'client_name': client_name,
                                                                'banks': banks,
                                                                'loggedInUser': loggedInUser,
                                                                'cash': cash,
                                                                'page_title': page_title,'wrn': wrn,
                                                                'text': text,
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
        loggedInUser = admin_user.Name
        if admin_user.Active:
            if admin_admin:
                display = render(request, 'add_admin.html', {'admin': admin,
                                                             'loggedInUser': loggedInUser,
                                                             'admin_admin': admin_admin})
            else:
                display = render(request, 'access_denied.html', {'admin': admin,
                                                                 'loggedInUser': loggedInUser,
                                                                 'admin_admin': admin_admin})
        else:
            logout(request)
            display = render(request, 'login.html',
                             {'wrong': True,
                              'text': 'You are not authorized to login. Please contact administrator for more details'})
    else:
        display = redirect('/')
    return display


@login_required(login_url='/login/')
def add_client(request):
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
        loggedInUser = admin_user.Name
        if admin_user.Active:
            if admin_admin:
                display = render(request, 'add_client.html', {'admin': admin,
                                                              'page_title': '|Add A Client|',
                                                              'loggedInUser': loggedInUser,
                                                              'admin_admin': admin_admin})
            else:
                display = render(request, 'access_denied.html', {'admin': admin,
                                                                 'page_title': '|Access Denied|',
                                                                 'loggedInUser': loggedInUser,
                                                                 'admin_admin': admin_admin})
        else:
            logout(request)
            display = render(request, 'login.html',
                             {'wrong': True,
                              'text': 'You are not authorized to login. Please contact administrator for more details'})
    else:
        display = redirect('/')
    return display


@login_required(login_url='/login/')
def admin_list(request):
    user = request.session['user']
    # if admin
    if AdminUser.objects.filter(username__exact=user).exists():
        admin = True
        admin_user = AdminUser.objects.get(username__exact=user)
        admin_admin = admin_user.Admin
        loggedInUser = admin_user.Name
        if admin_user.Active and admin_admin:
            all_admin_users = AdminUser.objects.all()
            display = render(request, 'admin_list.html',
                             {'admin': admin,
                              'admin_admin': admin_admin,
                              'loggedInUser': loggedInUser,
                              'page_title': '|List Of Admins|',
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


@login_required(login_url='/login/')
def client_list(request):
    user = request.session['user']
    # if admin
    if AdminUser.objects.filter(username__exact=user).exists():
        admin = True
        admin_user = AdminUser.objects.get(username__exact=user)
        admin_admin = admin_user.Admin
        loggedInUser = admin_user.Name
        if admin_user.Active:
            all_client_users = Client.objects.all()
            display = render(request, 'client_list.html',
                             {'admin': admin,
                              'all_client_users': all_client_users,
                              'loggedInUser': loggedInUser,
                              'page_title': '|List Of Clients|',
                              'admin_admin': admin_admin})
        else:
            logout(request)
            display = render(request, 'login.html',
                             {'wrong': True,
                              'text': 'You are not authorized to login.'
                                      ' Please contact administrator for more details'})
    else:
        display = redirect('/')
    return display


@login_required(login_url='/login/')
def client_users_list(request):
    user = request.session['user']
    # if client
    if ClientUser.objects.filter(username__exact=user).exists():
        client = True
        client_user = ClientUser.objects.get(username__exact=user)
        client_admin = client_user.Admin
        client_object = client_user.Client
        loggedInUser = client_user.Name
        all_users_of_client = ClientUser.objects.filter(Client=client_object)
        if client_user.Active:
            display = render(request, 'client_user_list.html', {'all_client': all_users_of_client,
                                                                'client': client,
                                                                'loggedInUser': loggedInUser,
                                                                'page_title': '|Client User List|',
                                                                'client_admin': client_admin})
        else:
            logout(request)
            display = render(request, 'login.html',
                             {'wrong': True,
                              'text': 'You are not authorized to login. Please contact administrator for more details'})
    else:
        display = render(request, 'access_denied.html',
                         {'wrong': True,
                          'text': 'Something went wrong. Please LOGIN again.'})
    return display


@login_required(login_url='/login/')
def add_new_client_user(request):
    user = request.session['user']
    # if client
    if ClientUser.objects.filter(username__exact=user).exists():
        client = True
        client_user = ClientUser.objects.get(username__exact=user)
        client_admin = client_user.Admin
        client_object = client_user.Client
        all_users_of_client = ClientUser.objects.filter(Client=client_object)
        loggedInUser = client_user.Name
        if client_user.Active:
            if client_user.Admin:
                display = render(request, 'add_new_client_user.html', {'all_client': all_users_of_client,
                                                                       'client': client,
                                                                       'loggedInUser': loggedInUser,
                                                                       'page_title': '|Add A New User|',
                                                                       'client_admin': client_admin})
            else:
                display = render(request, 'access_denied.html', {'all_client': all_users_of_client,
                                                                 'client': client,
                                                                 'loggedInUser': loggedInUser,
                                                                 'page_title': '|Add A New User|',
                                                                 'client_admin': client_admin})
        else:
            logout(request)
            display = render(request, 'login.html',
                             {'wrong': True,
                              'text': 'You are not authorized to login. Please contact administrator for more details'})
    else:
        display = render(request, 'access_denied.html',
                         {'wrong': True,
                          'text': 'Something went wrong. Please LOGIN again.'})
    return display


@login_required(login_url='/login/')
def transaction_by_date(request):
    user = request.session['user']
    # if client
    if ClientUser.objects.filter(username__exact=user).exists():
        client = True
        client_user = ClientUser.objects.get(username__exact=user)
        client_admin = client_user.Admin
        client_object = client_user.Client
        loggedInUser = client_user.Name
        all_users_of_client = ClientUser.objects.filter(Client=client_object)
        if client_user.Active:
            if 'start_date' in request.POST and 'stop_date' in request.POST:
                start_date = request.POST['start_date']
                stop_date = request.POST['stop_date']
                timeframe = start_date + ' and ' + stop_date
                trans = Transaction.objects.filter(DateAdded__range=[start_date, stop_date], Client=client_object)
                display = render(request, 'transaction_by_date.html', {'all_client': all_users_of_client,
                                                                       'client': client,
                                                                       'page_title': 'Transactions',
                                                                       'trans': trans,
                                                                       'loggedInUser': loggedInUser,
                                                                       'selected': True,
                                                                       'timeframe': timeframe,
                                                                       'client_admin': client_admin})
            else:
                display = render(request, 'transaction_by_date.html', {'all_client': all_users_of_client,
                                                                       'client': client,
                                                                       'loggedInUser': loggedInUser,
                                                                       'page_title': '|Add A New User|',
                                                                       'client_admin': client_admin})
        else:
            logout(request)
            display = render(request, 'login.html',
                             {'wrong': True,
                              'text': 'You are not authorized to login. Please contact administrator for more details'})
    else:
        display = render(request, 'access_denied.html',
                         {'wrong': True,
                          'text': 'Something went wrong. Please LOGIN again.'})
    return display


@login_required(login_url='/login/')
def profile(request):
    page_title = '|Profile|'
    user = request.session['user']
    # if admin
    if AdminUser.objects.filter(username__exact=user).exists():
        admin = True
        admin_user = AdminUser.objects.get(username__exact=user)
        admin_admin = admin_user.Admin
        loggedinuser = admin_user.Name
        username = user
        email = admin_user.Email
        phone = admin_user.Phone
        active = admin_user.Active
        isadmin = admin_user.Admin
        joined_since = admin_user.DateAdded
        if admin_user.Active:
            display = render(request, 'profile.html', {'admin': admin,
                                                       'loggedInUser': loggedinuser,
                                                       'page_title': page_title,
                                                       'admin_admin': admin_admin,
                                                       'username': username,
                                                       'email': email,
                                                       'phone': phone,
                                                       'active': active,
                                                       'isadmin': isadmin,
                                                       'joined_since': joined_since})
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
        loggedinuser = client_user.Name
        client_name = client_user.Client.ClientName
        if client_user.Active:
            client_object = client_user.Client
            username = user
            email = client_user.Email
            phone = client_user.Phone
            active = client_user.Active
            isadmin = client_user.Admin
            joined_since = client_user.DateAdded
            company_address = client_object.Address

            display = render(request, 'profile.html', {'client': client,
                                                       'client_name': client_name,
                                                       'loggedInUser': loggedinuser,
                                                       'page_title': page_title,
                                                       'client_admin': client_admin,
                                                       'username': username,
                                                       'email': email,
                                                       'phone': phone,
                                                       'active': active,
                                                       'isadmin': isadmin,
                                                       'joined_since': joined_since,
                                                       'company_address': company_address})
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
def change_password(request):
    page_title = '|Change Password|'
    user = request.session['user']
    post_data = request.POST
    wrong = False
    text = ''
    # if admin
    if 'csrfmiddlewaretoken' in post_data:
        if post_data['password'] == post_data['re-password']:
            if User.objects.filter(username=user).exists():
                u = User.objects.get(username=user)
                u.set_password(post_data['password'])
                u.save()
                wrong = True
                text = 'Password is successfully changed'
            else:
                wrong = True
                text = 'Something Wrong'
        else:
            wrong = True
            text = 'Passwords do NOT match. Please try again'

    if AdminUser.objects.filter(username__exact=user).exists():
        admin = True
        admin_user = AdminUser.objects.get(username__exact=user)
        admin_admin = admin_user.Admin
        loggedinuser = admin_user.Name
        if admin_user.Active:
            display = render(request, 'changePassword.html', {'admin': admin,
                                                              'loggedInUser': loggedinuser,
                                                              'page_title': page_title,
                                                              'admin_admin': admin_admin,
                                                              'wrong': wrong,
                                                              'text': text})
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
        loggedinuser = client_user.Name
        client_name = client_user.Client.ClientName
        if client_user.Active:
            display = render(request, 'changePassword.html', {'client': client,
                                                              'client_name': client_name,
                                                              'loggedInUser': loggedinuser,
                                                              'page_title': page_title,
                                                              'client_admin': client_admin,
                                                              'wrong': wrong,
                                                              'text': text})
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


@csrf_exempt
def forgot_password(request):
    postdata = request.POST
    print(postdata)
    if 'username' in postdata:
        username = postdata['username']
        if User.objects.filter(username=username).exists():
            u = User.objects.get(username=username)
            useremail = u.email

        else:
            res = render(request, 'login.html',
                         {'wrong': True,
                          'text': 'Something went wrong. Please try again'})
    else:
        res = render(request, 'login.html', {'wrong': False})

    res['Access-Control-Allow-Origin'] = "*"
    res['Access-Control-Allow-Headers'] = "Origin, X-Requested-With, Content-Type, Accept"
    res['Access-Control-Allow-Methods'] = "PUT, GET, POST, DELETE, OPTIONS"
    return res


@login_required(login_url='/login/')
def new_transaction(request):
    page_title = 'New Transaction'
    loggedInUser = ''
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
        loggedInUser = admin_user.Name
        if admin_user.Active:
            display = render(request, 'dashboard.html', {'admin': admin,
                                                         'loggedInUser': loggedInUser,
                                                         'page_title': page_title,
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
        loggedInUser = client_user.Name
        client_name = client_user.Client.ClientName
        if client_user.Active:
            client_object = client_user.Client
            banks = Bank.objects.filter(ClientName=client_object, Active=True)
            cash = Cash.objects.get(ClientName=client_object)
            suggestion_name = ClientUserSuggestionNames.objects.filter(Client=client_object)
            suggestion_purpose = ClientUserSuggestionPurpose.objects.filter(Client=client_object)

            list_transaction = Transaction.objects.filter(Client=client_object)

            received_transaction = Transaction.objects.filter(Client=client_object, Received=True)
            paid_transaction = Transaction.objects.filter(Client=client_object, Received=False)
            borrowed_transaction = BorrowedTransaction.objects.filter(transaction=Transaction.objects.filter(Client=client_object), Paid=False)
            borrowed_transaction_paid = BorrowedTransaction.objects.filter(transaction=Transaction.objects.filter(Client=client_object), Paid=True)
            lent_transaction = LentTransaction.objects.filter(transaction=Transaction.objects.filter(Client=client_object), Paid=False)
            lent_transaction_paid = LentTransaction.objects.filter(transaction=Transaction.objects.filter(Client=client_object), Paid=True)
            if 'err' in request.GET and request.GET['err'] == '1':
                wrn = True
                text = 'Insufficient Balance'
            else:
                wrn = False
                text = ''
            display = render(request, 'new_transaction.html', {'client': client,
                                                               'client_name': client_name,
                                                               'banks': banks,
                                                               'loggedInUser': loggedInUser,
                                                               'cash': cash,
                                                               'page_title': page_title,
                                                               'new_transaction_active': True,
                                                               # 'list_transaction': list_transaction,
                                                               # 'received_transaction': received_transaction,
                                                               # 'paid_transaction': paid_transaction,
                                                               'suggestion_name': suggestion_name,
                                                               'suggestion_purpose': suggestion_purpose,
                                                               # 'borrowed_transaction': borrowed_transaction,
                                                               # 'borrowed_transaction_paid': borrowed_transaction_paid,
                                                               # 'lent_transaction': lent_transaction,
                                                               # 'lent_transaction_paid': lent_transaction_paid,
                                                               'wrn': wrn,
                                                               'text': text,
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
def all_transaction(request):
    page_title = 'All Transaction'
    loggedInUser = ''
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
        loggedInUser = admin_user.Name
        if admin_user.Active:
            display = render(request, 'dashboard.html', {'admin': admin,
                                                         'loggedInUser': loggedInUser,
                                                         'page_title': page_title,
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
        loggedInUser = client_user.Name
        client_name = client_user.Client.ClientName
        if client_user.Active:
            client_object = client_user.Client
            banks = Bank.objects.filter(ClientName=client_object, Active=True)
            cash = Cash.objects.get(ClientName=client_object)
            suggestion_name = ClientUserSuggestionNames.objects.filter(Client=client_object)
            suggestion_purpose = ClientUserSuggestionPurpose.objects.filter(Client=client_object)

            list_transaction = Transaction.objects.filter(Client=client_object)

            received_transaction = Transaction.objects.filter(Client=client_object, Received=True)
            paid_transaction = Transaction.objects.filter(Client=client_object, Received=False)
            borrowed_transaction = BorrowedTransaction.objects.filter(transaction=Transaction.objects.filter(Client=client_object), Paid=False)
            borrowed_transaction_paid = BorrowedTransaction.objects.filter(transaction=Transaction.objects.filter(Client=client_object), Paid=True)
            lent_transaction = LentTransaction.objects.filter(transaction=Transaction.objects.filter(Client=client_object), Paid=False)
            lent_transaction_paid = LentTransaction.objects.filter(transaction=Transaction.objects.filter(Client=client_object), Paid=True)
            if 'err' in request.GET and request.GET['err'] == '1':
                wrn = True
                text = 'Insufficient Balance'
            else:
                wrn = False
                text = ''
            display = render(request, 'all_transaction.html', {'client': client,
                                                               'client_name': client_name,
                                                               'banks': banks,
                                                               'loggedInUser': loggedInUser,
                                                               'cash': cash,
                                                               'page_title': page_title,
                                                               'list_transaction': list_transaction,
                                                               'all_transaction_active': True,
                                                               # 'received_transaction': received_transaction,
                                                               # 'paid_transaction': paid_transaction,
                                                               'suggestion_name': suggestion_name,
                                                               'suggestion_purpose': suggestion_purpose,
                                                               # 'borrowed_transaction': borrowed_transaction,
                                                               # 'borrowed_transaction_paid': borrowed_transaction_paid,
                                                               # 'lent_transaction': lent_transaction,
                                                               # 'lent_transaction_paid': lent_transaction_paid,
                                                               'wrn': wrn,
                                                               'text': text,
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
def rec_transaction(request):
    page_title = 'Money Received'
    loggedInUser = ''
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
        loggedInUser = admin_user.Name
        if admin_user.Active:
            display = render(request, 'dashboard.html', {'admin': admin,
                                                         'loggedInUser': loggedInUser,
                                                         'page_title': page_title,
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
        loggedInUser = client_user.Name
        client_name = client_user.Client.ClientName
        if client_user.Active:
            client_object = client_user.Client
            banks = Bank.objects.filter(ClientName=client_object, Active=True)
            cash = Cash.objects.get(ClientName=client_object)
            suggestion_name = ClientUserSuggestionNames.objects.filter(Client=client_object)
            suggestion_purpose = ClientUserSuggestionPurpose.objects.filter(Client=client_object)

            list_transaction = Transaction.objects.filter(Client=client_object)

            received_transaction = Transaction.objects.filter(Client=client_object, Received=True)
            paid_transaction = Transaction.objects.filter(Client=client_object, Received=False)
            borrowed_transaction = BorrowedTransaction.objects.filter(transaction=Transaction.objects.filter(Client=client_object), Paid=False)
            borrowed_transaction_paid = BorrowedTransaction.objects.filter(transaction=Transaction.objects.filter(Client=client_object), Paid=True)
            lent_transaction = LentTransaction.objects.filter(transaction=Transaction.objects.filter(Client=client_object), Paid=False)
            lent_transaction_paid = LentTransaction.objects.filter(transaction=Transaction.objects.filter(Client=client_object), Paid=True)
            if 'err' in request.GET and request.GET['err'] == '1':
                wrn = True
                text = 'Insufficient Balance'
            else:
                wrn = False
                text = ''
            display = render(request, 'rec_transaction.html', {'client': client,
                                                               'client_name': client_name,
                                                               'banks': banks,
                                                               'loggedInUser': loggedInUser,
                                                               'cash': cash,
                                                               'page_title': page_title,
                                                               # 'list_transaction': list_transaction,
                                                               'received_transaction': received_transaction,
                                                               # 'paid_transaction': paid_transaction,
                                                               'suggestion_name': suggestion_name,
                                                               'rec_transaction_active': True,
                                                               'suggestion_purpose': suggestion_purpose,
                                                               # 'borrowed_transaction': borrowed_transaction,
                                                               # 'borrowed_transaction_paid': borrowed_transaction_paid,
                                                               # 'lent_transaction': lent_transaction,
                                                               # 'lent_transaction_paid': lent_transaction_paid,
                                                               'wrn': wrn,
                                                               'text': text,
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
def paid_transaction(request):
    page_title = 'Money Paid'
    loggedInUser = ''
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
        loggedInUser = admin_user.Name
        if admin_user.Active:
            display = render(request, 'dashboard.html', {'admin': admin,
                                                         'loggedInUser': loggedInUser,
                                                         'page_title': page_title,
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
        loggedInUser = client_user.Name
        client_name = client_user.Client.ClientName
        if client_user.Active:
            client_object = client_user.Client
            banks = Bank.objects.filter(ClientName=client_object, Active=True)
            cash = Cash.objects.get(ClientName=client_object)
            suggestion_name = ClientUserSuggestionNames.objects.filter(Client=client_object)
            suggestion_purpose = ClientUserSuggestionPurpose.objects.filter(Client=client_object)

            list_transaction = Transaction.objects.filter(Client=client_object)

            received_transaction = Transaction.objects.filter(Client=client_object, Received=True)
            paid_transaction = Transaction.objects.filter(Client=client_object, Received=False)
            borrowed_transaction = BorrowedTransaction.objects.filter(transaction=Transaction.objects.filter(Client=client_object), Paid=False)
            borrowed_transaction_paid = BorrowedTransaction.objects.filter(transaction=Transaction.objects.filter(Client=client_object), Paid=True)
            lent_transaction = LentTransaction.objects.filter(transaction=Transaction.objects.filter(Client=client_object), Paid=False)
            lent_transaction_paid = LentTransaction.objects.filter(transaction=Transaction.objects.filter(Client=client_object), Paid=True)
            if 'err' in request.GET and request.GET['err'] == '1':
                wrn = True
                text = 'Insufficient Balance'
            else:
                wrn = False
                text = ''
            display = render(request, 'paid_transaction.html', {'client': client,
                                                                'client_name': client_name,
                                                                'banks': banks,
                                                                'loggedInUser': loggedInUser,
                                                                'cash': cash,
                                                                'page_title': page_title,
                                                                # 'list_transaction': list_transaction,
                                                                # 'received_transaction': received_transaction,
                                                                'paid_transaction': paid_transaction,
                                                                'paid_transaction_active': True,
                                                                'suggestion_name': suggestion_name,
                                                                'suggestion_purpose': suggestion_purpose,
                                                                # 'borrowed_transaction': borrowed_transaction,
                                                                # 'borrowed_transaction_paid': borrowed_transaction_paid,
                                                                # 'lent_transaction': lent_transaction,
                                                                # 'lent_transaction_paid': lent_transaction_paid,
                                                                'wrn': wrn,
                                                                'text': text,
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
def borrowed_transaction(request):
    page_title = 'Borrowed Transaction'
    loggedInUser = ''
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
        loggedInUser = admin_user.Name
        if admin_user.Active:
            display = render(request, 'dashboard.html', {'admin': admin,
                                                         'loggedInUser': loggedInUser,
                                                         'page_title': page_title,
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
        loggedInUser = client_user.Name
        client_name = client_user.Client.ClientName
        if client_user.Active:
            client_object = client_user.Client
            banks = Bank.objects.filter(ClientName=client_object, Active=True)
            cash = Cash.objects.get(ClientName=client_object)
            suggestion_name = ClientUserSuggestionNames.objects.filter(Client=client_object)
            suggestion_purpose = ClientUserSuggestionPurpose.objects.filter(Client=client_object)

            list_transaction = Transaction.objects.filter(Client=client_object)

            received_transaction = Transaction.objects.filter(Client=client_object, Received=True)
            paid_transaction = Transaction.objects.filter(Client=client_object, Received=False)
            borrowed_transaction = BorrowedTransaction.objects.filter(transaction=Transaction.objects.filter(Client=client_object), Paid=False)
            borrowed_transaction_paid = BorrowedTransaction.objects.filter(transaction=Transaction.objects.filter(Client=client_object), Paid=True)
            lent_transaction = LentTransaction.objects.filter(transaction=Transaction.objects.filter(Client=client_object), Paid=False)
            lent_transaction_paid = LentTransaction.objects.filter(transaction=Transaction.objects.filter(Client=client_object), Paid=True)
            if 'err' in request.GET and request.GET['err'] == '1':
                wrn = True
                text = 'Insufficient Balance'
            else:
                wrn = False
                text = ''
            display = render(request, 'borrowed_transaction.html', {'client': client,
                                                                    'client_name': client_name,
                                                                    'banks': banks,
                                                                    'loggedInUser': loggedInUser,
                                                                    'cash': cash,
                                                                    'page_title': page_title,
                                                                    # 'list_transaction': list_transaction,
                                                                    # 'received_transaction': received_transaction,
                                                                    'borrowed_transaction_active': True,
                                                                    # 'paid_transaction': paid_transaction,
                                                                    'suggestion_name': suggestion_name,
                                                                    'suggestion_purpose': suggestion_purpose,
                                                                    'borrowed_transaction': borrowed_transaction,
                                                                    'borrowed_transaction_paid': borrowed_transaction_paid,
                                                                    # 'lent_transaction': lent_transaction,
                                                                    # 'lent_transaction_paid': lent_transaction_paid,
                                                                    'wrn': wrn,
                                                                    'text': text,
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
def lent_transaction(request):
    page_title = 'Lent Transaction'
    loggedInUser = ''
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
        loggedInUser = admin_user.Name
        if admin_user.Active:
            display = render(request, 'dashboard.html', {'admin': admin,
                                                         'loggedInUser': loggedInUser,
                                                         'page_title': page_title,
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
        loggedInUser = client_user.Name
        client_name = client_user.Client.ClientName
        if client_user.Active:
            client_object = client_user.Client
            banks = Bank.objects.filter(ClientName=client_object, Active=True)
            cash = Cash.objects.get(ClientName=client_object)
            suggestion_name = ClientUserSuggestionNames.objects.filter(Client=client_object)
            suggestion_purpose = ClientUserSuggestionPurpose.objects.filter(Client=client_object)

            list_transaction = Transaction.objects.filter(Client=client_object)

            received_transaction = Transaction.objects.filter(Client=client_object, Received=True)
            paid_transaction = Transaction.objects.filter(Client=client_object, Received=False)
            borrowed_transaction = BorrowedTransaction.objects.filter(transaction=Transaction.objects.filter(Client=client_object), Paid=False)
            borrowed_transaction_paid = BorrowedTransaction.objects.filter(transaction=Transaction.objects.filter(Client=client_object), Paid=True)
            lent_transaction = LentTransaction.objects.filter(transaction=Transaction.objects.filter(Client=client_object), Paid=False)
            lent_transaction_paid = LentTransaction.objects.filter(transaction=Transaction.objects.filter(Client=client_object), Paid=True)
            if 'err' in request.GET and request.GET['err'] == '1':
                wrn = True
                text = 'Insufficient Balance'
            else:
                wrn = False
                text = ''
            display = render(request, 'lent_transaction.html', {'client': client,
                                                                    'client_name': client_name,
                                                                    'banks': banks,
                                                                    'loggedInUser': loggedInUser,
                                                                    'cash': cash,
                                                                    'page_title': page_title,
                                                                    # 'list_transaction': list_transaction,
                                                                    # 'received_transaction': received_transaction,
                                                                    # 'paid_transaction': paid_transaction,
                                                                    'suggestion_name': suggestion_name,
                                                                    'suggestion_purpose': suggestion_purpose,
                                                                    'lent_transaction_active': True,
                                                                    # 'borrowed_transaction': borrowed_transaction,
                                                                    # 'borrowed_transaction_paid': borrowed_transaction_paid,
                                                                    'lent_transaction': lent_transaction,
                                                                    'lent_transaction_paid': lent_transaction_paid,
                                                                    'wrn': wrn,
                                                                    'text': text,
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
def banks(request):
    page_title = 'Lent Transaction'
    loggedInUser = ''
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
        loggedInUser = admin_user.Name
        if admin_user.Active:
            display = render(request, 'dashboard.html', {'admin': admin,
                                                         'loggedInUser': loggedInUser,
                                                         'page_title': page_title,
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
        loggedInUser = client_user.Name
        client_name = client_user.Client.ClientName
        if client_user.Active:
            client_object = client_user.Client
            banks = Bank.objects.filter(ClientName=client_object, Active=True)
            cash = Cash.objects.get(ClientName=client_object)
            suggestion_name = ClientUserSuggestionNames.objects.filter(Client=client_object)
            suggestion_purpose = ClientUserSuggestionPurpose.objects.filter(Client=client_object)

            list_transaction = Transaction.objects.filter(Client=client_object)

            received_transaction = Transaction.objects.filter(Client=client_object, Received=True)
            paid_transaction = Transaction.objects.filter(Client=client_object, Received=False)
            borrowed_transaction = BorrowedTransaction.objects.filter(transaction=Transaction.objects.filter(Client=client_object), Paid=False)
            borrowed_transaction_paid = BorrowedTransaction.objects.filter(transaction=Transaction.objects.filter(Client=client_object), Paid=True)
            lent_transaction = LentTransaction.objects.filter(transaction=Transaction.objects.filter(Client=client_object), Paid=False)
            lent_transaction_paid = LentTransaction.objects.filter(transaction=Transaction.objects.filter(Client=client_object), Paid=True)
            if 'err' in request.GET and request.GET['err'] == '1':
                wrn = True
                text = 'Insufficient Balance'
            else:
                wrn = False
                text = ''
            display = render(request, 'banks.html', {'client': client,
                                                                    'client_name': client_name,
                                                                    'banks': banks,
                                                                    'loggedInUser': loggedInUser,
                                                                    'cash': cash,
                                                                    'page_title': page_title,
                                                                    # 'list_transaction': list_transaction,
                                                                    # 'received_transaction': received_transaction,
                                                                    # 'paid_transaction': paid_transaction,
                                                                    'suggestion_name': suggestion_name,
                                                                    'suggestion_purpose': suggestion_purpose,
                                                                    'banks_active': True,
                                                                    # 'borrowed_transaction': borrowed_transaction,
                                                                    # 'borrowed_transaction_paid': borrowed_transaction_paid,
                                                                    'lent_transaction': lent_transaction,
                                                                    'lent_transaction_paid': lent_transaction_paid,
                                                                    'wrn': wrn,
                                                                    'text': text,
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

@csrf_exempt
def test(request):
    return render(request, 'test.html')
