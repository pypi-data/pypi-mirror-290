from django.contrib import admin
from django.urls import path
from django.urls import path,re_path,include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
import debug_toolbar
from.url_base import get_url_patterns as get_url_patterns_base
from.url_spartaqube import get_url_patterns as get_url_patterns_spartaqube
handler404='project.sparta_e937f475e2.sparta_668469a095.qube_72d08bb252.sparta_4ca8ff63c3'
handler500='project.sparta_e937f475e2.sparta_668469a095.qube_72d08bb252.sparta_af898bede8'
handler403='project.sparta_e937f475e2.sparta_668469a095.qube_72d08bb252.sparta_4137dd01d2'
handler400='project.sparta_e937f475e2.sparta_668469a095.qube_72d08bb252.sparta_8e322477d2'
urlpatterns=get_url_patterns_base()+get_url_patterns_spartaqube()
if settings.B_TOOLBAR:urlpatterns+=[path('__debug__/',include(debug_toolbar.urls))]