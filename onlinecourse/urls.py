from django.urls import path
from . import views

app_name = 'onlinecourse'
urlpatterns = [
    # ... (giữ nguyên các URL cũ ở đây)
    
    # Định tuyến cho submit
    path('<int:course_id>/submit/', views.submit, name='submit'),
    
    # Định tuyến cho show_exam_result
    path('course/<int:course_id>/submission/<int:submission_id>/result/', views.show_exam_result, name='show_exam_result'),
]