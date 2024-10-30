from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('', index, name='index'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('employee-dashboard/', employee_dashboard, name='employee_dashboard'),
    path('logout/', logout_view, name='logout'),
    path('calendar/', calendar_view, name='calendar'),
    path('calendar/add/', add_task, name='add_task'),
    path('calendar/edit/', edit_task, name='edit_task'),
    path('add-task/', add_task, name='add_task'),
    path('edit_task/<int:task_id>/', edit_task, name='edit_task'),
    path('delete_task/<int:task_id>/', delete_task, name='delete_task'),
    path('view_task', view_task, name='view_task'),
    path('', index, name='index'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('sign-in/', sign_in_view, name='sign_in'),
    path('sign-out/', sign_out_view, name='sign_out'),
    path('salary_record/', attendance_report, name = 'salary_record'),
    path('employee_salary_overview/', attendance_overview_view, name = 'employee_salary_overview'),
    path('edit_employee/<int:user_id>/', edit_employee_view, name='edit_employee'),
]
