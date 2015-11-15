from django.conf.urls import patterns, include, url
from Wallet.views import *
from django.contrib.auth.views import login,logout,password_change,password_change_done

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'STP_Project.views.home', name='home'),
    # url(r'^STP_Project/', include('STP_Project.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^registration/$', clientRegistration),
    url(r'^ok/$',ok),
    url(r'^login/$',login),
    url(r'^accounts/login/$',login),
    url(r'^logout/$',logout, {'next_page': '/'}),
    #url(r'^users/$',userslist),
    #url(r'^wallets/$',wallets_list),
    url(r'^register/$',register),
    url(r'^moneytransfer/$',money_transfer),
    url(r'^nuts/$',nuts),
    url(r'^bonus/$',bonus),
    url(r'^confirm/$',confirm),
    url(r'^confirm/([0-9A-Za-z]{32,32})', email_confirm),
    url(r'^profile/password-changed$',password_change_done),
    url(r'^profile/change_password/$', 'django.contrib.auth.views.password_change', {'post_change_redirect': '/profile/password-changed'}),
    #url(r'^money/add/\d{1,2}/$',money_add)
    url(r'^$', mainpage),

)
