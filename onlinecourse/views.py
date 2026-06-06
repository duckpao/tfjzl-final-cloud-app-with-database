from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .models import Course, Enrollment, Submission, Choice

def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        # Lấy bản ghi Enrollment của user cho khóa học này
        enrollment = Enrollment.objects.get(user=request.user, course=course)
        # Tạo mới một Submission
        submission = Submission.objects.create(enrollment=enrollment)
        
        # Lấy tất cả các lựa chọn (choices) mà user đã tick
        for key, value in request.POST.items():
            if key.startswith('choice_'):
                choice_id = value
                choice = Choice.objects.get(pk=choice_id)
                submission.choices.add(choice)
        
        submission.save()
        # Chuyển hướng sang trang kết quả
        return redirect('onlinecourse:show_exam_result', course_id=course.id, submission_id=submission.id)

def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    
    # Tính điểm (tùy thuộc vào logic môn học, đây là mẫu cơ bản)
    total_questions = course.question_set.count()
    correct_answers = 0
    
    for question in course.question_set.all():
        # Lấy các đáp án đúng của câu hỏi
        correct_choices = set(question.choice_set.filter(is_correct=True).values_list('id', flat=True))
        # Lấy các đáp án user đã chọn cho câu hỏi này
        user_choices = set(submission.choices.filter(question=question).values_list('id', flat=True))
        
        # Nếu user chọn đúng hoàn toàn các đáp án
        if correct_choices == user_choices:
            correct_answers += 1
            
    score = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
    passed = score >= 70 # Yêu cầu pass là 70%
    
    context = {
        'course': course,
        'score': score,
        'passed': passed,
    }
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)