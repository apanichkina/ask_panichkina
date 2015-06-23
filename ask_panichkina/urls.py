from django.conf.urls import patterns, include, url
from django.contrib import admin
from ask_panichkina.views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ask_panichkina.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    #url(r'^helloworld/', 'ask_panichkina.views.helloworld', name='helloworld'),
    url(r'^(\w*)$', index, name='index'),
    url(r'^tag/(.+)$', sortbytag, name='tag'),
    url(r'^signup/$', signup, name='signup'),
    #url(r'^signup/$', register, name='register'),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', log_out, name='logout'),
    url(r'^ask_question/$', ask_question, name='ask_question'),
    url(r'^question/(\d+)/$', question, name='question'),
    url(r'^profile/(.+)$', profile, name='profile')
)