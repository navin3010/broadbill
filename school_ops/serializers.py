from . import models
from rest_framework import serializers

class GroupSerializer(serializers.ModelSerializer):
    group_id = serializers.ReadOnlyField(source = "id")
    class Meta:
        model = models.Groups
        fields = ["group_id", "name", "is_active"]


class WriteGroupNameSerializer(serializers.ModelSerializer):
    group_id = serializers.ReadOnlyField(source="id")

    class Meta:
        model = models.Groups
        fields = ["group_id", "name"]

    def check_record_if_exists(self, data: dict):
        name = data.get("name", "")
        group = models.Groups.objects.filter(name=name)
        if group:
            raise serializers.ValidationError(
                {
                    "result": False,
                    "msg": "Group Name already added",
                },
                code="validation_error",
            )


class SubjectSerializer(serializers.ModelSerializer):
    subject_id = serializers.ReadOnlyField(source = "id")
    class Meta:
        model = models.Subjects
        fields = ["subject_id", "title", "is_active"]


class WriteSubjectSerializer(serializers.ModelSerializer):
    subject_id = serializers.ReadOnlyField(source="id")

    class Meta:
        model = models.Subjects
        fields = ["subject_id", "title"]

    def check_record_if_exists(self, data: dict):
        title = data.get("title", "").lower()
        subject = models.Subjects.objects.filter(title=title)
        if subject:
            raise serializers.ValidationError(
                {
                    "result": False,
                    "msg": "subject name already added",
                },
                code="validation_error",
            )

'''
"data": {
        "teacher_id": 3,
        "group_id": 4,
        "subject_id": 5,
        "is_active": true
    }
'''
class TeacherSerializer(serializers.ModelSerializer):
    teacher_id = serializers.ReadOnlyField(source = "id")
    subject = SubjectSerializer()
    group = GroupSerializer()

    class Meta:
        model = models.Teachers
        fields = ["teacher_id","is_active", "subject", "group"]


class WriteTeacherSerializer(serializers.ModelSerializer):
    teacher_id = serializers.ReadOnlyField(source="id")

    class Meta:
        model = models.Teachers
        fields = ["teacher_id", "group_id", "subject_id", "is_active"]

    def check_record_if_exists(self, data: dict):
        group_id = data.get("group_id", "")
        subject_id = data.get("subject_id", "")
        subject = models.Teachers.objects.filter(group_id = group_id, subject_id = subject_id)
        if subject:
            raise serializers.ValidationError(
                {
                    "result": False,
                    "msg": "teacher already added for mentioned group",
                },
                code="validation_error",
            )
        
class WriteStudentSerializer(serializers.ModelSerializer):
    student_id = serializers.ReadOnlyField(source="id")

    class Meta:
        model = models.Students
        fields = ["student_id", "first_name", "last_name", "is_active"]

    def check_record_if_exists(self, data: dict):
        first_name = data.get("first_name", "")
        last_name = data.get("last_name", "")
        group_id = data.get("group_id", "")
        student = models.Students.objects.filter(
            first_name = first_name,
            last_name = last_name,
            group_id = group_id)
        if student:
            raise serializers.ValidationError(
                {
                    "result": False,
                    "msg": "student name already added",
                },
                code="validation_error",
            )

class StudentSerializer(serializers.ModelSerializer):
    student_id = serializers.ReadOnlyField(source = "id")
    group = GroupSerializer()

    class Meta:
        model = models.Students
        fields = ["student_id","is_active", "group"]

class WriteMarks(serializers.ModelSerializer):
    mark_id = serializers.ReadOnlyField(source="id")

    class Meta:
        model = models.Marks
        fields = ["mark_id", "student_id", "subject_id", "mark", "date", "is_active"]

    def check_record_if_exists(self, data: dict):
        student_id = data.get("student_id", "")
        subject_id = data.get("subject_id", "")
        mark = data.get("mark", "")
        student = models.Marks.objects.filter(
            student_id = student_id,
            subject_id = subject_id,
            mark = mark)
        if student:
            raise serializers.ValidationError(
                {
                    "result": False,
                    "msg": "student record with given deatils exists",
                },
                code="validation_error",
            )
        
class WriteMarksReadOnlySerializer(serializers.ModelSerializer):
    mark_id = serializers.ReadOnlyField(source="id")
    student = StudentSerializer()

    class Meta:
        model = models.Marks
        fields = ["mark_id","subject_id", "student", "mark", "date", "is_active"]

class WriteMarksWithSubjectsReadOnlySerializer(serializers.ModelSerializer):
    mark_id = serializers.ReadOnlyField(source="id")
    student = StudentSerializer()
    subject = SubjectSerializer()

    class Meta:
        model = models.Marks
        fields = ["mark_id","subject", "student", "mark", "date", "is_active"]