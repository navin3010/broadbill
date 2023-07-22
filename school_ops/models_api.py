from . import models
from django.core import exceptions
from rest_framework import serializers as rest_serializers

class GroupsModel:
    def get_group_details_by_id(self, group_id:int):
        try:
            group_data = models.Groups.objects.get(id = group_id, is_active=True)
        except exceptions.ObjectDoesNotExist:
            raise rest_serializers.ValidationError(
                {
                    "result": False,
                    "msg": "Invalid group_id"},
                code="validation_error",
            )
        return group_data
    
    def get_all_group_details(self, is_active=True):
        try:
            all_group_data = models.Groups.objects.filter(is_active=is_active)
        except exceptions.ObjectDoesNotExist:
            raise rest_serializers.ValidationError(
                {
                    "result": False,
                    "msg": "Invalid group_id"},
                code="validation_error",
            )
        return all_group_data

class SubjectModel:
    def get_subject_details_by_id(self, subject_id:int):
        try:
            subject_data = models.Subjects.objects.get(id = subject_id, is_active=True)
        except exceptions.ObjectDoesNotExist:
            raise rest_serializers.ValidationError(
                {
                    "result": False,
                    "msg": "Invalid subject_id"},
                code="validation_error",
            )
        return subject_data
    
    def get_all_subject_details(self, is_active=True):
        try:
            all_subject_data = models.Subjects.objects.filter(is_active=is_active)
        except exceptions.ObjectDoesNotExist:
            raise rest_serializers.ValidationError(
                {
                    "result": False,
                    "msg": "Invalid subject_id"},
                code="validation_error",
            )
        return all_subject_data
    
    def check_subject_is_active(self, subject_id):
        try:
            print("try")
            subject_is_active = models.Subjects.objects.get(id = subject_id, is_active=True)
            print("subject_is_active", subject_is_active)
        except exceptions.ObjectDoesNotExist:
            raise rest_serializers.ValidationError(
                {
                    "result": False,
                    "msg": "Invalid subject_id"},
                code="validation_error",
            )
        return subject_is_active
    
class TeacherModel:
    def get_teacher_details_by_id(self, teacher_id:int):
        try:
            teacher_data = models.Teachers.objects.select_related(
                "group").select_related(
                "subject").filter(id = teacher_id, is_active=True)
        except exceptions.ObjectDoesNotExist:
            raise rest_serializers.ValidationError(
                {
                    "result": False,
                    "msg": "Invalid subject_id"},
                code="validation_error",
            )
        return teacher_data

class StudentModel:

    def check_student_is_active_using_student_id(self, student_id):
        try:
            models.Students.objects.get(id = student_id, is_active = True)
        except exceptions.ObjectDoesNotExist:
            raise rest_serializers.ValidationError(
                {
                    "result": False,
                    "msg": "Student is not present"},
                code="validation_error",
            )
        # return subject_is_active
    def get_student_details_by_id(self, student_id:int):
        try:
            # student_data = models.Students.objects.get(id = student_id)
            student_data = models.Students.objects.select_related("group").filter(
                id = student_id
            )
        except exceptions.ObjectDoesNotExist:
            raise rest_serializers.ValidationError(
                {
                    "result": False,
                    "msg": "Invalid subject_id"},
                code="validation_error",
            )
        return student_data
    

class MarkModels:
    def get_mark_details_by_id(self, mark_id: int):
        try:
            mark_data = models.Marks.objects.get(id = mark_id, is_active = True)
        except exceptions.ObjectDoesNotExist:
            raise rest_serializers.ValidationError(
                {
                    "result": False,
                    "msg": "Invalid mark_id"},
                code="validation_error",
            )
        return mark_data
    
    def get_mark_details_by_student_id(self, student_id: int):
        try:
            mark_data = models.Marks.objects.select_related("student").filter(
                student_id = student_id, is_active=True)
        except exceptions.ObjectDoesNotExist:
            raise rest_serializers.ValidationError(
                {
                    "result": False,
                    "msg": "Invalid mark_id"},
                code="validation_error",
            )
        return mark_data
    
    def get_mark_details_with_subjects_by_student_id(self, student_id: int):
        try:
            mark_data = models.Marks.objects.select_related("student", "subject").filter(
                student_id = student_id, is_active=True)
        except exceptions.ObjectDoesNotExist:
            raise rest_serializers.ValidationError(
                {
                    "result": False,
                    "msg": "Invalid mark_id"},
                code="validation_error",
            )
        return mark_data

