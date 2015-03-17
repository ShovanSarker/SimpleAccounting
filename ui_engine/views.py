from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from admin_user_panel.models import AdminUser
from client_user_panel.models import Client, ClientUser, ClientUserSuggestionNames, ClientUserSuggestionPurpose
from cash.models import Cash
from bank.models import Bank
from transaction.models import Transaction, BorrowedTransaction, LentTransaction
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
            display = render(request, 'client_dashboard.html', {'client': client,
                                                                'client_name': client_name,
                                                                'banks': banks,
                                                                'cash': cash,
                                                                'list_transaction': list_transaction,
                                                                'received_transaction': received_transaction,
                                                                'paid_transaction': paid_transaction,
                                                                'suggestion_name': suggestion_name,
                                                                'suggestion_purpose': suggestion_purpose,
                                                                'borrowed_transaction': borrowed_transaction,
                                                                'borrowed_transaction_paid': borrowed_transaction_paid,
                                                                'lent_transaction': lent_transaction,
                                                                'lent_transaction_paid': lent_transaction_paid,
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
        if admin_user.Active:
            if admin_admin:
                display = render(request, 'add_client.html', {'admin': admin,
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


@login_required(login_url='/login/')
def admin_list(request):
    user = request.session['user']
    # if admin
    if AdminUser.objects.filter(username__exact=user).exists():
        admin = True
        admin_user = AdminUser.objects.get(username__exact=user)
        admin_admin = admin_user.Admin
        if admin_user.Active and admin_admin:
            all_admin_users = AdminUser.objects.all()
            display = render(request, 'admin_list.html',
                             {'admin': admin,
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


@login_required(login_url='/login/')
def client_list(request):
    user = request.session['user']
    # if admin
    if AdminUser.objects.filter(username__exact=user).exists():
        admin = True
        admin_user = AdminUser.objects.get(username__exact=user)
        admin_admin = admin_user.Admin
        if admin_user.Active:
            all_client_users = Client.objects.all()
            display = render(request, 'client_list.html',
                             {'admin': admin,
                              'all_client_users': all_client_users,
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
        all_users_of_client = ClientUser.objects.filter(Client=client_object)
        if client_user.Active:
            display = render(request, 'client_user_list.html', {'all_client': all_users_of_client,
                                                                'client': client,
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