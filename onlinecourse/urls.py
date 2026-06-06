from django.urls import path
from . import views

app_name = 'onlinecourse'
urlpatterns = [
    # Các router mặc định của dự án giữ nguyên...
    path('', views.CourseListView.as_view(), name='index'),
    path('course/<int:pk>/', views.CourseDetailView.as_view(), name='course_details'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('registration/', views.registration_request, name='registration'),
    
    # Thêm 2 đường dẫn xử lý tính năng thi
    path('course/<int:course_id>/submit/', views.submit, name='submit'),
    path('course/<int:course_id>/submission/<int:submission_id>/result/', views.show_exam_result, name='show_exam_result'),
]