from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Course, Lesson, Question, Choice, Submission, Enrollment

# --- Các view cũ như danh sách khóa học, login, logout giữ nguyên ---

# View xử lý khi học viên ấn nút "Submit Exam"
def submit(request, course_id):
    context = {}
    if request.method == 'POST':
        course = get_object_or_404(Course, pk=course_id)
        # Lấy thông tin đăng ký lớp học của user hiện tại
        enrollment = get_object_or_404(Enrollment, course=course, user=request.user)
        
        # Tạo một bản ghi Submission mới
        submission = Submission.objects.create(enrollment=enrollment)
        
        # Duyệt qua các dữ liệu POST gửi lên để gom các ID đáp án được chọn
        selected_ids = []
        for key, value in request.POST.items():
            if key.startswith('choice_'):
                selected_ids.append(int(value))
                choice = get_object_or_404(Choice, pk=int(value))
                submission.choices.add(choice)
        
        submission.save()
        # Điều hướng sang trang hiển thị kết quả
        return redirect('onlinecourse:show_exam_result', course_id=course.id, submission_id=submission.id)
    
    return redirect('onlinecourse:course_details', course_id=course_id)


# View tính toán điểm số và hiển thị kết quả bài thi
def show_exam_result(request, course_id, submission_id):
    context = {}
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    
    # Tính tổng số điểm tối đa của tất cả các câu hỏi trong khóa học
    max_score = sum([question.grade for question in course.question_set.all()])
    
    # Lấy danh sách ID các đáp án học viên đã chọn
    selected_ids = [choice.id for choice in submission.choices.all()]
    
    # Tính điểm đạt được bằng cách duyệt từng câu hỏi
    total_score = 0
    for question in course.question_set.all():
        if question.is_get_score(selected_ids):
            total_score += question.grade
            
    # Kiểm tra xem có đạt (Pass) từ 70% trở lên không
    percentage = (total_score / max_score) * 100 if max_score > 0 else 0
    passed = percentage >= 70
    
    # Đóng gói dữ liệu chuyển sang template hiển thị
    context['course'] = course
    context['submission'] = submission
    context['total_score'] = total_score
    context['max_score'] = max_score
    context['percentage'] = percentage
    context['passed'] = passed
    
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)