from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
 
    path('', views.home, name='home'),
    path('reg/',views.reg,name='reg'),
    path('token_send/',views.token_send,name='token_send'),
    path('verify/<auth_token>',views.verify,name='verify'),
    path('login/',views.login_view,name='login'),
    path('reset/<auth_token>',views.reset_pass,name='reset_pass'),
    path('forget_pass/',views.Forget_pass,name='forget_pass'),
  

]