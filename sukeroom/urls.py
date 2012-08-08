from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'rooms.views.index'),
    url(r'^search/', 'rooms.views.search'),
    url(r'^addcompany/', 'rooms.views.addcompany'),
    url(r'^company/(?P<company_id>\d+)', 'rooms.views.company'),
    url(r'^api/company/edit/$', 'rooms.views.company_edit'),
    url(r'^api/question/add/$', 'rooms.views.question_add'),
    url(r'^api/company/add/$', 'rooms.views.company_add'),
    url(r'^admin/', include(admin.site.urls)),
)
