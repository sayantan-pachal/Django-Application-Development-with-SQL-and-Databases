from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

# Application namespace for reverse URL resolution
app_name = 'onlinecourse'

urlpatterns = [
    # Standard application paths
    path('', views.CourseListView.as_view(), name='index'),
    path('registration/', views.registration_request, name='registration'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('course/<int:pk>/', views.CourseDetailView.as_view(), name='course_details'),
    path('course/<int:course_id>/enroll/', views.enroll, name='enroll'),

    # Assessment / Exam routing
    # Handles exam form POST submissions
    path('<int:course_id>/submit/', views.submit, name='submit'),
    # Displays the exam grading results
    path('<int:course_id>/submission/<int:submission_id>/result/', views.show_exam_result, name='show_exam_result'),
    # Compatibility alias for templates or test suites referencing exam_result
    path('<int:course_id>/submission/<int:submission_id>/exam_result/', views.show_exam_result, name='exam_result'),
]

# Serve media files in development environment
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
