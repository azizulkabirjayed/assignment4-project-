from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('faculty_dashboard/', views.faculty_dashboard, name='faculty_dashboard'),
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('logout/', views.logout_view, name='logout'),

    path('admin_dashboard/notice_board/', views.notice_board, name='notice_board'),
    path('admin_dashboard/add_notice/', views.add_notice, name='add_notice'),
    path('admin_dashboard/add_faculty/', views.add_faculty, name='add_faculty'),
    path('admin_dashboard/faculty_list/', views.faculty_list, name='faculty_list'),
    path('admin_dashboard/delete_notice/<int:notice_id>/', views.notice_board, name='delete_notice'),
    path('admin_dashboard/delete_faculty/<int:user_id>/', views.faculty_list, name='delete_faculty'),
    
]