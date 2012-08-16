from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'rooms.views.index'),
    url(r'^search/', 'rooms.views.search'),
    url(r'^companylist/', 'rooms.views.companylist'),
    url(r'^questionlist/', 'rooms.views.questionlist'),
    url(r'^qalist/', 'rooms.views.qalist'),
    url(r'^statistics/', 'rooms.views.statistics'),
    url(r'^ranking/', 'rooms.views.ranking'),
    url(r'^addcompany/', 'rooms.views.addcompany'),
    url(r'^editcompany/(?P<company_id>\d+)/', 'rooms.views.editcompany'),
    url(r'^company/(?P<company_id>\d+)/', 'rooms.views.company'),
    url(r'^question/(?P<question_id>\d+)/', 'rooms.views.question'),
    url(r'^api/answer/edit/$', 'rooms.views.answer_edit'),
    url(r'^api/question/add/$', 'rooms.views.question_add'),
    url(r'^api/company/add/$', 'rooms.views.company_add'),
    url(r'^api/company/edit/$', 'rooms.views.company_edit'),
    url(r'^api/piedata/(?P<question_id>\d+)/$', 'rooms.views.piedata'),
    url(r'^admin/', include(admin.site.urls)),
)
