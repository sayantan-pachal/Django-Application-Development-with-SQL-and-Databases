from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic, View
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .models import Course, Lesson, Enrollment, Question, Choice, Submission


# Class-based view for displaying the list of courses
class CourseListView(generic.ListView):
    template_name = 'onlinecourse/course_list.html'
    context_object_name = 'course_list'

    def get_queryset(self):
        return Course.objects.order_by('-total_enrollment')


# Class-based view for displaying course details along with lessons and the assessment form
class CourseDetailView(generic.DetailView):
    model = Course
    template_name = 'onlinecourse/course_details_bootstrap.html'
    context_object_name = 'course'


# View to handle course enrollment
def enroll(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.user.is_authenticated:
        enrollment, created = Enrollment.objects.get_or_create(
            user=request.user,
            course=course,
            defaults={'mode': Enrollment.AUDIT}
        )
        if created:
            course.total_enrollment += 1
            course.save()
    return redirect('onlinecourse:course_details', pk=course.id)


# Assessment Submit View: processes exam submissions
def submit(request, course_id):
    """
    Processes the POST request from the course detail exam form.
    Extracts the selected choice radio button answers, creates a Submission record,
    associates the selected choices, and redirects to the exam result page.
    """
    course = get_object_or_404(Course, pk=course_id)

    if request.method == 'POST':
        # Retrieve selected choices from POST payload
        # Forms render radio buttons as choice_<question.id> = <choice.id>
        selected_choice_ids = []
        for key, value in request.POST.items():
            if key.startswith('choice_') or key.startswith('question_'):
                try:
                    selected_choice_ids.append(int(value))
                except (ValueError, TypeError):
                    pass

        # Also iterate directly over course questions to ensure all radio groups are captured
        for question in course.question_set.all():
            field_name = f"choice_{question.id}"
            if field_name in request.POST:
                try:
                    choice_id = int(request.POST[field_name])
                    if choice_id not in selected_choice_ids:
                        selected_choice_ids.append(choice_id)
                except (ValueError, TypeError):
                    pass

        # Get or link enrollment if user is authenticated
        enrollment = None
        if request.user.is_authenticated:
            enrollment = Enrollment.objects.filter(user=request.user, course=course).first()
            if not enrollment:
                enrollment = Enrollment.objects.create(user=request.user, course=course)

        # Create a Submission record for this exam attempt
        submission = Submission.objects.create(
            course=course,
            enrollment=enrollment
        )

        # Retrieve and assign the chosen Choice records to the submission
        selected_choices = Choice.objects.filter(id__in=selected_choice_ids)
        submission.choices.set(selected_choices)
        submission.save()

        # Redirect to the show_exam_result view
        return redirect('onlinecourse:show_exam_result', course_id=course.id, submission_id=submission.id)

    # If accessed via GET, redirect back to course details
    return redirect('onlinecourse:course_details', pk=course.id)


# Assessment Result View: calculates score and renders result template
def show_exam_result(request, course_id, submission_id):
    """
    Fetches the submission and course, calculates total possible points and points earned,
    computes the percentage grade, determines pass/fail status (threshold >= 70%),
    and passes rich context to exam_result.html.
    """
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id, course=course)

    questions = course.question_set.all()
    selected_choice_ids = set(submission.choices.values_list('id', flat=True))

    total_score = 0
    earned_score = 0
    detailed_results = []

    for question in questions:
        total_score += question.grade
        
        # Check if the user's answer is correct using question.is_get_score
        is_correct = question.is_get_score(selected_choice_ids)
        points_earned = question.grade if is_correct else 0
        earned_score += points_earned

        # Retrieve the user's selected choice for this specific question
        selected_choice = submission.choices.filter(question=question).first()

        detailed_results.append({
            'question': question,
            'selected_choice': selected_choice,
            'is_correct': is_correct,
            'grade': question.grade,
            'points_earned': points_earned,
            'choices': question.choice_set.all()
        })

    # Calculate percentage score
    if total_score > 0:
        grade = round((earned_score / total_score) * 100, 1)
    else:
        grade = 0.0

    # Passing requirement is 70%
    passed = grade >= 70.0

    context = {
        'course': course,
        'submission': submission,
        'grade': grade,
        'score': grade,
        'earned_score': earned_score,
        'total_score': total_score,
        'passed': passed,
        'selected_ids': selected_choice_ids,
        'detailed_results': detailed_results,
    }
    return render(request, 'onlinecourse/exam_result.html', context)


# User Authentication Views
def registration_request(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome to Online Course, {user.username}!")
            return redirect('onlinecourse:index')
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
    else:
        form = UserCreationForm()
    return render(request, 'onlinecourse/user_registration.html', {'form': form})


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Logged in as {user.username}.")
            return redirect('onlinecourse:index')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'onlinecourse/user_login.html', {'form': form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('onlinecourse:index')
