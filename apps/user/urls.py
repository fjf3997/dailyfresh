from django.conf.urls import url
from apps.user import views

urlpatterns = [
    # url('^register$', views.register, name='register'),
    # url('^register_handler$', views.register_handler, name='register_handler')
    url('^register$', views.RegisterView.as_view(), name='register'),
    url('^login$', views.LoginView.as_view(), name='login'),
    url('^active/(?P<token>.*)$', views.ActiveView.as_view(), name='active'),
]
