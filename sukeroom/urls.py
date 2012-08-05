from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^company/', 'rooms.views.company'),
    url(r'^api/company/edit/', 'rooms.views.company_edit'),
    url(r'^api/question/add/', 'rooms.views.question_add'),
    url(r'^admin/', include(admin.site.urls)),
)
