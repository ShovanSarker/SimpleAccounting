from django.shortcuts import render, redirect
from client_user_panel.models import ClientUser
from django.contrib.auth import authenticate, login, logout
from .models import Transaction, BorrowedTransaction, LentTransaction
from bank.models import Bank
from cash.models import Cash
from client_user_panel.models import ClientUserSuggestionNames, ClientUserSuggestionPurpose

# Create your views here.


def receive_money(request):
    if 'user' in request.session:
        user = request.session['user']
        print(request.POST)
        # if client
        if ClientUser.objects.filter(username__exact=user).exists():
            client_user = ClientUser.objects.get(username__exact=user)
            client_object = client_user.Client
            if client_user.Active:
                post_data = request.POST
                if 'csrfmiddlewaretoken' in post_data:
                    next_date = post_data['next_date']
                    name = post_data['name']
                    if not ClientUserSuggestionNames.objects.filter(Client=client_object, ClientNameSuggestion=name):
                        new_name_suggestion = ClientUserSuggestionNames(Client=client_object, ClientNameSuggestion=name)
                        new_name_suggestion.save()
                    amount = float(post_data['amount'])
                    purpose = post_data['purpose']
                    if not ClientUserSuggestionPurpose.objects.filter(Client=client_object,
                                                                      ClientPurposeSuggestion=purpose):
                        new_purpose_suggestion = ClientUserSuggestionPurpose(Client=client_object,
                                                                             ClientPurposeSuggestion=purpose)
                        new_purpose_suggestion.save()
                    remarks = post_data['remarks']
                    t_type = post_data['type']
                    entry_by = client_user
                    if t_type == 'cash':
                        new_transaction = Transaction(Client=client_object,
                                                      Purpose=purpose,
                                                      TransactionWith=name,
                                                      Amount=amount,
                                                      Remarks=remarks,
                                                      Type='Cash',
                                                      EntryBy=entry_by)
                        cash_update = Cash.objects.get(ClientName=client_object)
                        cash_update.Balance += amount
                        cash_update.save()
                    else:
                        bank = Bank.objects.get(id=post_data['type'])
                        new_transaction = Transaction(Client=client_object,
                                                      Purpose=purpose,
                                                      TransactionWith=name,
                                                      Amount=amount,
                                                      Remarks=remarks,
                                                      Type='Bank',
                                                      Bank=bank,
                                                      EntryBy=entry_by)
                        bank.Balance += amount
                        bank.save()
                    new_transaction.save()
                    if 'loan' in post_data and post_data['loan'] == 'on':
                        if next_date == '':
                            new_borrowed_transaction = BorrowedTransaction(transaction=new_transaction)
                        else:
                            new_borrowed_transaction = BorrowedTransaction(transaction=new_transaction,
                                                                           NextDate=next_date)
                        new_borrowed_transaction.save()
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


def pay_money(request):
    if 'user' in request.session:
        user = request.session['user']
        print(request.POST)
        # if client
        if ClientUser.objects.filter(username__exact=user).exists():
            client_user = ClientUser.objects.get(username__exact=user)
            client_object = client_user.Client
            if client_user.Active:
                post_data = request.POST
                if 'csrfmiddlewaretoken' in post_data:
                    next_date = post_data['next_date']
                    name = post_data['name']
                    if not ClientUserSuggestionNames.objects.filter(Client=client_object, ClientNameSuggestion=name):
                        new_name_suggestion = ClientUserSuggestionNames(Client=client_object, ClientNameSuggestion=name)
                        new_name_suggestion.save()
                    amount = float(post_data['amount'])
                    purpose = post_data['purpose']
                    if not ClientUserSuggestionPurpose.objects.filter(Client=client_object,
                                                                      ClientPurposeSuggestion=purpose):
                        new_purpose_suggestion = ClientUserSuggestionPurpose(Client=client_object,
                                                                             ClientPurposeSuggestion=purpose)
                        new_purpose_suggestion.save()
                    remarks = post_data['remarks']
                    t_type = post_data['type']
                    entry_by = client_user
                    if t_type == 'cash':
                        cash_update = Cash.objects.get(ClientName=client_object)
                        if amount <= cash_update.Balance:
                            new_transaction = Transaction(Client=client_object,
                                                          Purpose=purpose,
                                                          TransactionWith=name,
                                                          Amount=amount,
                                                          Remarks=remarks,
                                                          Type='Cash',
                                                          Received=False,
                                                          EntryBy=entry_by)
                            cash_update.Balance -= amount
                            cash_update.save()
                            new_transaction.save()
                            if 'loan' in post_data and post_data['loan'] == 'on':
                                if next_date == '':
                                    new_borrowed_transaction = LentTransaction(transaction=new_transaction)
                                else:
                                    new_borrowed_transaction = LentTransaction(transaction=new_transaction,
                                                                               NextDate=next_date)
                                new_borrowed_transaction.save()
                        else:
                            text = 'insufficient balance!'
                    else:
                        bank = Bank.objects.get(id=post_data['type'])
                        if amount <= bank.Balance:
                            new_transaction = Transaction(Client=client_object,
                                                          Purpose=purpose,
                                                          TransactionWith=name,
                                                          Amount=amount,
                                                          Remarks=remarks,
                                                          Type='Bank',
                                                          Received=False,
                                                          Bank=bank,
                                                          EntryBy=entry_by)
                            bank.Balance -= amount
                            bank.save()
                            new_transaction.save()
                            if 'loan' in post_data and post_data['loan'] == 'on':
                                if next_date == '':
                                    new_borrowed_transaction = LentTransaction(transaction=new_transaction)
                                else:
                                    new_borrowed_transaction = LentTransaction(transaction=new_transaction,
                                                                               NextDate=next_date)
                                new_borrowed_transaction.save()
                        else:
                            text = 'insufficient balance!'

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


def pay_due_money(request):
    if 'user' in request.session:
        user = request.session['user']
        print(request.GET)
        # if client
        if ClientUser.objects.filter(username__exact=user).exists():
            client_user = ClientUser.objects.get(username__exact=user)
            client_object = client_user.Client
            if client_user.Active:
                post_data = request.GET

                transaction_object = BorrowedTransaction.objects.get(id=post_data['due'])
                transaction_amount = transaction_object.transaction.Amount
                if post_data['type'] == 'cash':
                    balance = Cash.objects.get(ClientName=client_object).Balance
                    if balance > transaction_amount:
                        transaction_object.Paid = True
                        transaction_object.save()
                        new_transaction = Transaction(Client=client_object,
                                                      Purpose='Pay Due',
                                                      TransactionWith=transaction_object.transaction.TransactionWith,
                                                      Amount=transaction_object.transaction.Amount,
                                                      Type='Cash',
                                                      Received=False,
                                                      EntryBy=client_user)
                        new_transaction.save()
                        update_transaction = Cash.objects.get(ClientName=client_object)
                        update_transaction.Balance -= transaction_amount
                        update_transaction.save()
                    else:
                        text = 'insufficient balance'
                else:
                    balance = Bank.objects.get(id=post_data['type']).Balance
                    if balance > transaction_amount:
                        transaction_object.Paid = True
                        transaction_object.save()
                        new_transaction = Transaction(Client=client_object,
                                                      Purpose='Pay Due',
                                                      TransactionWith=transaction_object.transaction.TransactionWith,
                                                      Amount=transaction_object.transaction.Amount,
                                                      Type='Bank',
                                                      Bank=Bank.objects.get(id=post_data['type']),
                                                      Received=False,
                                                      EntryBy=client_user)
                        new_transaction.save()
                        update_transaction = Bank.objects.get(id=post_data['type'])
                        update_transaction.Balance -= transaction_amount
                        update_transaction.save()
                    else:
                        text = 'insufficient balance'
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


def rec_due_money(request):
    if 'user' in request.session:
        user = request.session['user']
        print(request.GET)
        # if client
        if ClientUser.objects.filter(username__exact=user).exists():
            client_user = ClientUser.objects.get(username__exact=user)
            client_object = client_user.Client
            if client_user.Active:
                post_data = request.GET

                transaction_object = LentTransaction.objects.get(id=post_data['due'])
                transaction_amount = transaction_object.transaction.Amount
                if post_data['type'] == 'cash':
                    transaction_object.Paid = True
                    transaction_object.save()
                    new_transaction = Transaction(Client=client_object,
                                                  Purpose='Receive Due',
                                                  TransactionWith=transaction_object.transaction.TransactionWith,
                                                  Amount=transaction_object.transaction.Amount,
                                                  Type='Cash',
                                                  Received=True,
                                                  EntryBy=client_user)
                    new_transaction.save()
                    update_transaction = Cash.objects.get(ClientName=client_object)
                    update_transaction.Balance += transaction_amount
                    update_transaction.save()
                else:
                    transaction_object.Paid = True
                    transaction_object.save()
                    new_transaction = Transaction(Client=client_object,
                                                  Purpose='Receive Due',
                                                  TransactionWith=transaction_object.transaction.TransactionWith,
                                                  Amount=transaction_object.transaction.Amount,
                                                  Type='Bank',
                                                  Bank=Bank.objects.get(id=post_data['type']),
                                                  Received=True,
                                                  EntryBy=client_user)
                    new_transaction.save()
                    update_transaction = Bank.objects.get(id=post_data['type'])
                    update_transaction.Balance += transaction_amount
                    update_transaction.save()
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
