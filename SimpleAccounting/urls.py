from django.conf.urls import patterns, include, url
from ui_engine.views import login_page, login_auth, home, logout_now, add_admin
from admin_user_panel.views import add_admin_info, admin_list
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
                       )

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
