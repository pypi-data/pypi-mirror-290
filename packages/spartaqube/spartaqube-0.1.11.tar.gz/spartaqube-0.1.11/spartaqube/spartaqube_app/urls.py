from django.contrib import admin
from django.urls import path
from django.urls import path,re_path,include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
import debug_toolbar
from.url_base import get_url_patterns as get_url_patterns_base
from.url_spartaqube import get_url_patterns as get_url_patterns_spartaqube
handler404='project.sparta_3a78016751.sparta_f0cf741098.qube_bdd3b83d9e.sparta_311f71fae0'
handler500='project.sparta_3a78016751.sparta_f0cf741098.qube_bdd3b83d9e.sparta_dc4d7c12d8'
handler403='project.sparta_3a78016751.sparta_f0cf741098.qube_bdd3b83d9e.sparta_d59c35445c'
handler400='project.sparta_3a78016751.sparta_f0cf741098.qube_bdd3b83d9e.sparta_225a42646b'
urlpatterns=get_url_patterns_base()+get_url_patterns_spartaqube()
if settings.B_TOOLBAR:urlpatterns+=[path('__debug__/',include(debug_toolbar.urls))]