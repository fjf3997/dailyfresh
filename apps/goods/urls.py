from django.conf.urls import url,include
from apps.goods import views
urlpatterns = [
    url('^$', views.index, name='index')
]
