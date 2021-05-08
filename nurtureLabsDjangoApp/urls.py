from django.conf.urls import url
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='app-home'),
    path('admin/', views.admin, name='admin'),
    path('admin/advisor/', views.insert_advisor, name='admin-advisor'),
    path('user/register/', views.user_register, name='user-register'),
    path('user/login/', views.user_login, name='user-login'),
    url(r'^user/(?P<user_id>\d+)/advisor/booking/', views.get_booking_list, name='get-booking-list'),
    url(r'^user/(?P<user_id>\d+)/advisor/(?P<advisor_id>\d+)', views.book_call_with_advisor, name='book-call-advisor'),
    url(r'^user/(?P<user_id>\d+)/advisor/', views.get_advisor_list, name='get-advisor-list'),

]