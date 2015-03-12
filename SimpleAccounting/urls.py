from django.conf.urls import patterns, include, url
from ui_engine.views import login_page, login_auth, home, logout_now, add_admin, add_client, \
    admin_list, client_list, client_users_list
from admin_user_panel.views import add_admin_info, admin_modification
from client_user_panel.views import add_client_info, client_modification, client_user_modification
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
                       )

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
