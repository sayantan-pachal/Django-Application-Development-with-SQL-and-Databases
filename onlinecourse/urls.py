from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from . import views

# Application namespace
app_name = 'onlinecourse'

# Course application routes
app_urlpatterns = [
    path('', views.CourseListView.as_view(), name='index'),
    path('registration/', views.registration_request, name='registration'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('course/<int:pk>/', views.CourseDetailView.as_view(), name='course_details'),
    path('course/<int:course_id>/enroll/', views.enroll, name='enroll'),

    # Assessment / Exam routing
    path('<int:course_id>/submit/', views.submit, name='submit'),
    path('<int:course_id>/submission/<int:submission_id>/result/', views.show_exam_result, name='show_exam_result'),
    path('<int:course_id>/submission/<int:submission_id>/exam_result/', views.show_exam_result, name='exam_result'),
]

# Root URLconf routes
urlpatterns = [
    path('admin/', admin.site.urls),
    # Mount namespaced application routes under /onlinecourse/
    path('onlinecourse/', include((app_urlpatterns, 'onlinecourse'))),
    # Redirect root / to /onlinecourse/
    path('', RedirectView.as_view(url='/onlinecourse/', permanent=False)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
