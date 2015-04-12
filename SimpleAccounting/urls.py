from django.conf.urls import patterns, include, url
from ui_engine.views import login_page, login_auth, home, logout_now, add_admin, add_client, \
    admin_list, client_list, client_users_list, add_new_client_user, transaction_by_date,\
    profile, change_password, new_transaction, all_transaction, rec_transaction,\
    paid_transaction, borrowed_transaction,lent_transaction
from admin_user_panel.views import add_admin_info, admin_modification
from client_user_panel.views import add_client_info, client_modification, \
    client_user_modification, add_client_user_info
from transaction.views import receive_money, pay_money, pay_due_money, rec_due_money, transfer_money, buy_sell
from bank.views import add_a_bank
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^login/', view=login_page, name='home'),
                       url(r'^login_info/', view=login_auth, name='home'),
                       url(r'^$', view=home, name='home'),
                       url(r'^logout/', view=logout_now, name='home'),
                       url(r'^add_admin/', view=add_admin, name='home'),
                       url(r'^add_admin_info/', view=add_admin_info, name='home'),
                       url(r'^admin_list/', view=admin_list, name='home'),
                       url(r'^admin_modification/', view=admin_modification, name='home'),
                       url(r'^add_client/', view=add_client, name='home'),
                       url(r'^add_client_info/', view=add_client_info, name='home'),
                       url(r'^client_list/', view=client_list, name='home'),
                       url(r'^client_modification/', view=client_modification, name='home'),
                       url(r'^client_users_list/', view=client_users_list, name='home'),
                       url(r'^client_user_modification/', view=client_user_modification, name='home'),
                       url(r'^receive_money/', view=receive_money, name='home'),
                       url(r'^pay_money/', view=pay_money, name='home'),
                       url(r'^pay_due_money/', view=pay_due_money, name='home'),
                       url(r'^rec_due_money/', view=rec_due_money, name='home'),
                       url(r'^add_a_bank/', view=add_a_bank, name='home'),
                       url(r'^transfer_money/', view=transfer_money, name='home'),
                       url(r'^add_new_client_user/', view=add_new_client_user, name='home'),
                       url(r'^add_client_user_info/', view=add_client_user_info, name='home'),
                       url(r'^transaction_by_date/', view=transaction_by_date, name='home'),
                       url(r'^profile/', view=profile, name='home'),
                       url(r'^change_password/', view=change_password, name='home'),
                       url(r'^new_transaction/', view=new_transaction, name='home'),
                       url(r'^all_transaction/', view=all_transaction, name='home'),
                       url(r'^rec_transaction/', view=rec_transaction, name='home'),
                       url(r'^paid_transaction/', view=paid_transaction, name='home'),
                       url(r'^borrowed_transaction/', view=borrowed_transaction, name='home'),
                       url(r'^lent_transaction/', view=lent_transaction, name='home'),
                       url(r'^buy_sell/', view=buy_sell, name='home'),
                       )

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
