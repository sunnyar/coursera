from django.conf.urls import patterns, url
from .views import CourseListView, CourseDetailView, NewCourseListView

urlpatterns = patterns('',
        url(r'^courses/$', CourseListView.as_view(), name='course_list'),
        url(r'^new_courses/$', NewCourseListView.as_view(), name='new_course_list'),
        url(r'^courses/(?P<pk>[-\w\d]+)$', CourseDetailView.as_view(), name='course_detail'),
)