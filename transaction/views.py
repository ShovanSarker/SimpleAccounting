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
                            new_borrowed_transaction = BorrowedTransaction(transaction=new_transaction,
                                                                           RemainAmount=amount)
                        else:
                            new_borrowed_transaction = BorrowedTransaction(transaction=new_transaction,
                                                                           RemainAmount=amount,
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
                                    new_borrowed_transaction = LentTransaction(transaction=new_transaction,
                                                                               RemainAmount=amount)
                                else:
                                    new_borrowed_transaction = LentTransaction(transaction=new_transaction,
                                                                               RemainAmount=amount,
                                                                               NextDate=next_date)
                                new_borrowed_transaction.save()
                            display = redirect('/')
                        else:
                            display = redirect('/?err=1')
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
                            display = redirect('/')
                        else:
                            display = redirect('/?err=1')
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
                post_data = request.POST
                get_data = request.GET
                transaction_object = BorrowedTransaction.objects.get(id=get_data['due'])
                transaction_amount = float(post_data['amount'])
                if post_data['type'] == 'cash':
                    balance = Cash.objects.get(ClientName=client_object).Balance
                    if balance >= transaction_amount:
                        if transaction_object.RemainAmount <= transaction_amount:
                            transaction_object.Paid = True
                            transaction_object.RemainAmount = 0
                            transaction_object.save()
                        else:
                            transaction_object.RemainAmount -= transaction_amount
                            transaction_object.save()
                        new_transaction = Transaction(Client=client_object,
                                                      Purpose='Pay Due',
                                                      TransactionWith=transaction_object.transaction.TransactionWith,
                                                      Amount=transaction_amount,
                                                      Type='Cash',
                                                      Received=False,
                                                      EntryBy=client_user)
                        new_transaction.save()
                        update_transaction = Cash.objects.get(ClientName=client_object)
                        update_transaction.Balance -= transaction_amount
                        update_transaction.save()
                        display = redirect('/')
                    else:
                        display = redirect('/?err=1')
                else:
                    balance = Bank.objects.get(id=post_data['type']).Balance
                    if balance >= transaction_amount:
                        if transaction_object.RemainAmount <= transaction_amount:
                            transaction_object.Paid = True
                            transaction_object.RemainAmount = 0
                            transaction_object.save()
                        else:
                            transaction_object.RemainAmount -= transaction_amount
                            transaction_object.save()
                        new_transaction = Transaction(Client=client_object,
                                                      Purpose='Pay Due',
                                                      TransactionWith=transaction_object.transaction.TransactionWith,
                                                      Amount=transaction_amount,
                                                      Type='Bank',
                                                      Bank=Bank.objects.get(id=post_data['type']),
                                                      Received=False,
                                                      EntryBy=client_user)
                        new_transaction.save()
                        update_transaction = Bank.objects.get(id=post_data['type'])
                        update_transaction.Balance -= transaction_amount
                        update_transaction.save()
                        display = redirect('/')
                    else:
                        display = redirect('/?err=1')
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
                post_data = request.POST
                get_data = request.GET

                transaction_object = LentTransaction.objects.get(id=get_data['due'])
                transaction_amount = float(post_data['amount'])
                if post_data['type'] == 'cash':
                    if transaction_object.RemainAmount <= transaction_amount:
                        transaction_object.Paid = True
                        transaction_object.RemainAmount = 0
                        transaction_object.save()
                    else:
                        transaction_object.RemainAmount -= transaction_amount
                        transaction_object.save()
                    new_transaction = Transaction(Client=client_object,
                                                  Purpose='Receive Due',
                                                  TransactionWith=transaction_object.transaction.TransactionWith,
                                                  Amount=transaction_amount,
                                                  Type='Cash',
                                                  Received=True,
                                                  EntryBy=client_user)
                    new_transaction.save()
                    update_transaction = Cash.objects.get(ClientName=client_object)
                    update_transaction.Balance += transaction_amount
                    update_transaction.save()
                else:
                    if transaction_object.RemainAmount <= transaction_amount:
                        transaction_object.Paid = True
                        transaction_object.RemainAmount = 0
                        transaction_object.save()
                    else:
                        transaction_object.RemainAmount -= transaction_amount
                        transaction_object.save()
                    new_transaction = Transaction(Client=client_object,
                                                  Purpose='Receive Due',
                                                  TransactionWith=transaction_object.transaction.TransactionWith,
                                                  Amount=transaction_amount,
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


def transfer_money(request):
    if 'user' in request.session:
        user = request.session['user']
        print(request.GET)
        # if client
        if ClientUser.objects.filter(username__exact=user).exists():
            client_user = ClientUser.objects.get(username__exact=user)
            client_object = client_user.Client
            if client_user.Active:
                post_data = request.POST
                transfer_from = post_data['from']
                transfer_to = post_data['to']
                transfer_amount = float(post_data['amount'])
                if transfer_from == 'cash':
                    transfer_from_object = Cash.objects.get(ClientName=client_object)
                    from_name = transfer_from
                else:
                    transfer_from_object = Bank.objects.get(id=transfer_from)
                    from_name = transfer_from_object.NameOfTheBank

                if transfer_to == 'cash':
                    transfer_to_object = Cash.objects.get(ClientName=client_object)
                    to_name = transfer_to
                else:
                    transfer_to_object = Bank.objects.get(id=transfer_to)
                    to_name = transfer_to_object.NameOfTheBank
                if not transfer_amount > transfer_from_object.Balance:
                    transfer_from_object.Balance -= transfer_amount
                    transfer_to_object.Balance += transfer_amount
                    transfer_to_object.save()

                    transfer_from_object.save()
                    new_transaction = Transaction(Client=client_object,
                                                  Purpose='',
                                                  TransactionWith='Internal Transaction',
                                                  Amount=transfer_amount,
                                                  Type=from_name + ' to ' + to_name,
                                                  Received=True,
                                                  EntryBy=client_user)
                    new_transaction.save()
                    display = redirect('/')
                else:
                    display = redirect('/?err=1')
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


def buy_sell(request):
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
                    paid_amount = float(post_data['paidAmount'])
                    total_amount = float(post_data['totalAmount'])
                    due_amount = total_amount - paid_amount
                    # transaction_type = post_data['transactionType']
                    if not ClientUserSuggestionNames.objects.filter(Client=client_object, ClientNameSuggestion=name):
                        new_name_suggestion = ClientUserSuggestionNames(Client=client_object, ClientNameSuggestion=name)
                        new_name_suggestion.save()
                    purpose = post_data['transactionType'] + ' : ' + post_data['purpose']
                    remarks = post_data['remarks']
                    t_type = post_data['type']
                    entry_by = client_user

                    if post_data['transactionType'] == 'Sell':
                        receive = True
                        amount = paid_amount
                    else:
                        receive = False
                        amount = paid_amount * -1
                    if t_type == 'cash':
                        balance = Cash.objects.get(ClientName=client_object).Balance
                    else:
                        balance = Bank.objects.get(id=post_data['type']).Balance

                    if post_data['transactionType'] == 'Buy' and balance >= paid_amount:
                        if t_type == 'cash':
                            new_transaction = Transaction(Client=client_object,
                                                          Purpose=purpose,
                                                          TransactionWith=name,
                                                          Amount=paid_amount,
                                                          Remarks=remarks,
                                                          Type='Cash',
                                                          Received=receive,
                                                          EntryBy=entry_by)
                            cash_update = Cash.objects.get(ClientName=client_object)
                            cash_update.Balance += amount
                            cash_update.save()
                        else:
                            bank = Bank.objects.get(id=post_data['type'])
                            new_transaction = Transaction(Client=client_object,
                                                          Purpose=purpose,
                                                          TransactionWith=name,
                                                          Amount=paid_amount,
                                                          Remarks=remarks,
                                                          Type='Bank',
                                                          Bank=bank,
                                                          EntryBy=entry_by)
                            bank.Balance += amount
                            bank.save()
                        new_transaction.save()

                        if due_amount > 0:
                            if post_data['transactionType'] == 'Sell':
                                if next_date == '':
                                    new_due_transaction = LentTransaction(transaction=new_transaction,
                                                                          RemainAmount=due_amount)
                                else:
                                    new_due_transaction = LentTransaction(transaction=new_transaction,
                                                                          RemainAmount=due_amount,
                                                                          NextDate=next_date)
                                new_due_transaction.save()
                            elif post_data['transactionType'] == 'Buy':
                                if next_date == '':
                                    new_due_transaction = BorrowedTransaction(transaction=new_transaction,
                                                                              RemainAmount=due_amount)
                                else:
                                    new_due_transaction = BorrowedTransaction(transaction=new_transaction,
                                                                              RemainAmount=due_amount,
                                                                              NextDate=next_date)
                                new_due_transaction.save()
                        display = redirect('/')
                    else:
                        display = redirect('/?err=1')
                else:
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