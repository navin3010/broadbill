from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("group/", views.GroupsAPI.as_view(), name="groups"),
    path("subjects/", views.SubjectsAPI.as_view(), name="subjects"),
    path("teachers/", views.TeachersAPI.as_view(), name="teachers"),
    path("students/", views.StudentsAPI.as_view(), name="students"),
    path("marks/", views.MarksAPI.as_view(), name="marks"),
    path("marks/student-id/", views.MarksByStudentIdAPI.as_view(), name="marks-by-student-id"),
    path(
        "marks-with-each-subjects/student-id/",
        views.MarksWithSubjectsByStudentIdAPI.as_view(), name="marks-with-each-subjects"),
]