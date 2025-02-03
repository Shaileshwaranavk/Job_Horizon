from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='Home_Page'),
    path('register/', views.register, name='register'),
    path('accounts/login/', views.login_page, name='login_page'),
    path('profile/', views.user_profile, name='User_Profile'),
    path('job-openings/', views.job_openings_list, name='job_openings_list'),
    path('org_register/', views.org_registration, name='Organization_Register_Page'),
    path('org_login/', views.organization_login, name='Organization_Login_Page'),
    path('dashboard/', views.organization_dashboard, name='organization_dashboard'),
    path('create-job/<int:organization_id>/', views.create_job, name='create_job'),
    path('edit-job/<int:job_id>/', views.edit_job, name='edit_job'),
    path('delete-job/<int:job_id>/', views.delete_job, name='delete_job'),
    path('admin_page/',views.admin_login,name='admin_login'),
    path('admin_page/admin_dash/', views.dashboard, name='dashboard'),
    path('suggest_user_to_job/<int:job_id>/', views.suggest_user_to_job, name='suggest_user_to_job'),
]
