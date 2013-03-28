from django.conf.urls import patterns, include, url
from django.contrib import admin
# admin.autodiscover()
from codetests import views

urlpatterns = patterns('',
    url(r'^$', views.upload, name='home'),
    url(r'^upload/', views.upload, name='upload'),
    url(r'^response/', views.response, name='response'),
    # Examples:
    # url(r'^$', 'CodingTestVerification.views.home', name='home'),
    # url(r'^CodingTestVerification/', include('CodingTestVerification.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
