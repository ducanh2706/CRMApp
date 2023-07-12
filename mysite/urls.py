from django.urls import path
from . import views

app_name = 'mysite'

urlpatterns = [
    path('', views.home, name='home'),
    # path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('change_password/', views.change_password, name='change_password'),
    path('<int:pk>/', views.view_record, name='view_record'),
    path('add_record/', views.add_record, name='add_record'),
    path('<int:pk>/delete_record', views.delete_record, name='delete_record'),
    path('<int:pk>/update_record', views.update_record, name='update_record'),
]
