from django.contrib import admin
from django.urls import path
from django.urls import path,re_path,include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
import debug_toolbar
from.url_base import get_url_patterns as get_url_patterns_base
from.url_spartaqube import get_url_patterns as get_url_patterns_spartaqube
handler404='project.sparta_20d434a590.sparta_364af625e8.qube_cabfee7d6e.sparta_4251ad9856'
handler500='project.sparta_20d434a590.sparta_364af625e8.qube_cabfee7d6e.sparta_44b6a20217'
handler403='project.sparta_20d434a590.sparta_364af625e8.qube_cabfee7d6e.sparta_490ee5badc'
handler400='project.sparta_20d434a590.sparta_364af625e8.qube_cabfee7d6e.sparta_1c860381a9'
urlpatterns=get_url_patterns_base()+get_url_patterns_spartaqube()
if settings.B_TOOLBAR:urlpatterns+=[path('__debug__/',include(debug_toolbar.urls))]