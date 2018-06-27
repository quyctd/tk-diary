from django.conf.urls import url, include
from note import views

urlpatterns = [
    url(r'^$', views.index, name="home"),
    url(r'^class/(?P<pk>\d+)$', views.detail, name="detail"),
    url(r'^signup/$', views.signup, name="signup")
] 
