from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from exams import views

urlpatterns = [
    path('', views.frontpage),
    path('courses/', views.courselist),
    path('courses/add/', views.addcourse),
    path('courses/<int:course_id>/', views.courseview),
    path('courses/<int:course_id>/<path:_ignore>/', views.courseview),
    path('exams/<int:exam_id>/', views.examview),
    path('exams/<int:exam_id>/<path:_ignore>/delete', views.delete_exam),
    path('exams/<int:exam_id>/<path:_ignore>/edit', views.edit_exam),
    path('exams/<int:exam_id>/<path:_ignore>/', views.examview),
    path('exams/add/', views.addexam),
    path('examfile/<int:examfile_id>/delete', views.delete_examfile),

    # account stuff
    path('login/', auth_views.LoginView.as_view(template_name='account/login.html')),
    path('logout/', auth_views.LogoutView.as_view(next_page='/')),
    path('register/', views.register),
    path('account/', views.modifyaccount),
    path('ownexams/', views.accountexams),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    path('admin/', admin.site.urls),

    # serve uploaded exams in development mode (no-op if DEBUG=False)
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
]
