from django.contrib import admin
from django.urls import path,include

from .import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.landingpage,name='landingpage'),
    # path('login/',views.login,name='login'),
    path('test/<cust_id>',views.test,name='test'),
    # path('signup/',views.signup,name='signup'),
    path('mylogin/',views.mylogin,name='mylogin'),
    path('mysignup/',views.mysignup,name = 'mysignup'),
    path('landingpage/',views.landingpage,name='landingpage'),
    path('logout/',views.logoutpage,name='logout'),
]