from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework import permissions, response, status, serializers
from users import validators
from . import models, serializers as school_ops_serializers, validators as school_ops_validators, models_api
from . import custom_pagination

class GroupsAPI(APIView):
    permission_classes = [permissions.AllowAny]
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = (IsAuthenticated)
    def post(self, request):
        validators.validate_content_type(request)
        validate_group_name = school_ops_validators.ValidateGroup()
        validate_group_name.validate(request)

        serializer = school_ops_serializers.WriteGroupNameSerializer(
            data=request.data)
        if not serializer.is_valid():
            return response.Response(
                {
                    "result": False,
                    "msg": "Validation error",
                    "error": serializer._errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer.check_record_if_exists(data=request.data)
        name = request.data.get("name", "")
        serializer.save(name=name)
        return response.Response(
            {
                "result": True,
                "msg": "success",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )

    def put(self, request):
        validators.validate_content_type(request)
        data = request.data
        group_id = data.get("group_id", "")
        name = data.get("name", "")
        if not name:
            msg = "Group name is missing"
            raise serializers.ValidationError(
                {
                    "result": False,
                    "msg": msg,
                },
                code="validation_error",
            )
        if str(name).isdigit() is True:
            msg = "Name cannot be numbers"
            raise serializers.ValidationError(
                {
                    "result": False,
                    "msg": msg,
                },
                code="validation_error",
            )
        if not group_id:
            msg = "Group id is missing"
            raise serializers.ValidationError(
                {
                    "result": False,
                    "msg": msg,
                },
                code="validation_error",
            )
        if str(group_id).isdigit() is False:
            raise serializers.ValidationError(
                {
                    "result": False,
                    "msg": "group id must be number",
                },
                code="validation_error",
            )
        group_models = models_api.GroupsModel()
        group_data = group_models.get_group_details_by_id(group_id=group_id)
        serializer = school_ops_serializers.WriteGroupNameSerializer(group_data, data = request.data)
        if serializer.is_valid():
            serializer.save(name=name)
            return response.Response(
                {
                    "result": True,
                    "msg": "success",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        return response.Response(
            {
                "result": False,
                "msg": "Validation Error",
                "error": serializer._errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request):
        validators.validate_content_type(request)
        data = request.data
        group_id = data.get("group_id", "")
        if not group_id:
            msg = "Group id is missing"
            raise serializers.ValidationError(
                {
                    "result": False,
                    "msg": msg,
                },
                code="validation_error",
            )
        if str(group_id).isdigit() is False:
            raise serializers.ValidationError(
                {
                    "result": False,
                    "msg": "group id must be number",
                },
                code="validation_error",
            )
        group_models = models_api.GroupsModel()
        group_data = group_models.get_group_details_by_id(group_id=group_id)
        group_data.is_active = False
        group_data.save()
        return response.Response({
            "result": True,
            "msg": "success",
            "data": {"group_id": group_id}},
            status=status.HTTP_200_OK,
        )
    
    def get(self, request):
        validators.validate_content_type(request)
        data = request.data
        group_id = data.get("group_id", "")
        limit = data.get("limit", "")
        offset = data.get("offset", 0)

        pagination = custom_pagination.Pagination()

        if group_id:
            group_models = models_api.GroupsModel()
            group_data = group_models.get_group_details_by_id(group_id=group_id)
            print(group_data)
            serializerd_data = school_ops_serializers.GroupSerializer(group_data, many=False)
            return response.Response(
                {
                    "result": True,
                    "msg": "success",
                    "data": serializerd_data.data,
                },
                status=status.HTTP_200_OK,
            )
        else:
            group_models = models_api.GroupsModel()
            group_data = group_models.get_all_group_details(is_active=True)

            # serializerd_data = school_ops_serializers.GroupSerializer(group_data, many=True)

            serializerd_data, next_link = pagination.get_paginated_response(
                group_data,
                offset,
                limit,
                school_ops_serializers.GroupSerializer)
            
            return response.Response(
                {
                    "result": True,
                    "msg": "success",
                    "next_link": next_link,
                    "data": serializerd_data,
                },
                status=status.HTTP_200_OK,
            )


class SubjectsAPI(APIView):

    permission_classes = [permissions.AllowAny]
    def post(self, request):
        validators.validate_content_type(request)
        validate_subject_name = school_ops_validators.ValidateSubject()
        validate_subject_name.validate(request)

        serializer = school_ops_serializers.WriteSubjectSerializer(
            data=request.data)
        if not serializer.is_valid():
            return response.Response(
                {
                    "result": False,
                    "msg": "Validation error",
                    "error": serializer._errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer.check_record_if_exists(data=request.data)
        title = request.data.get("title", "")
        serializer.save(title=title.lower())
        return response.Response(
            {
                "result": True,
                "msg": "success",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )
    
    def put(self, request):
        validators.validate_content_type(request)
        data = request.data
        subject_id = data.get("subject_id", "")
        title = data.get("title", "").lower()
        if not title:
            msg = "subject title is missing"
            raise serializers.ValidationError(
                {
                    "result": False,
                    "msg": msg,
                },
                code="validation_error",
            )
        if str(title).isdigit() is True:
            msg = "title cannot be numbers"
            raise serializers.ValidationError(
                {
                    "result": False,
                    "msg": msg,
                },
                code="validation_error",
            )
        if not subject_id:
            msg = "subject_id is missing"
            raise serializers.ValidationError(
                {
                    "result": False,
                    "msg": msg,
                },
                code="validation_error",
            )
        if str(subject_id).isdigit() is False:
            raise serializers.ValidationError(
                {
                    "result": False,
                    "msg": "group id must be number",
                },
                code="validation_error",
            )
        subject_models = models_api.SubjectModel()
        subject_data = subject_models.get_subject_details_by_id(subject_id=subject_id)
        serializer_data = school_ops_serializers.WriteSubjectSerializer(subject_data, data = request.data)
        if serializer_data.is_valid():
            serializer_data.save(title = title)
            return response.Response(
                {
                    "result": True,
                    "msg": "success",
                    "data": serializer_data.data,
                },
                status=status.HTTP_200_OK,
            )
        return response.Response(
            {
                "result": False,
                "msg": "Validation Error",
                "error": serializer_data._errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request):
        validators.validate_content_type(request)
        data = request.data
        subject_id = data.get("subject_id", "")
        if not subject_id:
            msg = "subject_id is missing"
            raise serializers.ValidationError(
                {
                    "result": False,
                    "msg": msg,
                },
                code="validation_error",
            )
        if str(subject_id).isdigit() is False:
            raise serializers.ValidationError(
                {
                    "result": False,
                    "msg": "subject_id must be number",
                },
                code="validation_error",
            )
        subject_models = models_api.SubjectModel()
        subject_data = subject_models.get_subject_details_by_id(subject_id=subject_id)
        subject_data.is_active = False
        subject_data.save()
        return response.Response({
            "result": True,
            "msg": "success",
            "data": {"subject_id": subject_id}},
            status=status.HTTP_200_OK,
        )
    
    def get(self, request):
        validators.validate_content_type(request)
        data = request.data
        subject_id = data.get("subject_id", "")
        limit = data.get("limit", '')
        offset = data.get("offset", 0)
        if subject_id:
            subject_model = models_api.SubjectModel()
            subject_data = subject_model.get_subject_details_by_id(subject_id=subject_id)
            serializerd_data = school_ops_serializers.SubjectSerializer(subject_data, many=False)
            return response.Response(
                {
                    "result": True,
                    "msg": "success",
                    "data": serializerd_data.data,
                },
                status=status.HTTP_200_OK,
            )
        else:
            subject_model = models_api.SubjectModel()
            subject_data = subject_model.get_all_subject_details(is_active=True)
            # serializerd_data = school_ops_serializers.SubjectSerializer(subject_data, many=True)
            paginate = custom_pagination.Pagination()
            serialized_data, next_link = paginate.get_paginated_response(
                subject_data,
                offset,
                limit,
                school_ops_serializers.SubjectSerializer)
            return response.Response(
                {
                    "result": True,
                    "msg": "success",
                    "next_link" : next_link,
                    "data": serialized_data,
                },
                status=status.HTTP_200_OK,
            )


class TeachersAPI(APIView):

    permission_classes = [permissions.AllowAny]
    def post(self, request):
        validators.validate_content_type(request)
        validate_subject_name = school_ops_validators.ValidateTeacher()
        validate_subject_name.validate(request)

        serializer = school_ops_serializers.WriteTeacherSerializer(
            data=request.data)
        if not serializer.is_valid():
            return response.Response(
                {
                    "result": False,
                    "msg": "Validation error",
                    "error": serializer._errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer.check_record_if_exists(data=request.data)
        group_id = request.data.get("group_id", "")
        subject_id = request.data.get("subject_id", "")

        # subject_model = models_api.SubjectModel()
        # subject_model.check_subject_is_active(subject_id=subject_id)
        serializer.save(group_id = group_id, subject_id = subject_id)
        return response.Response(
            {
                "result": True,
                "msg": "success",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )
    
    def put(self, request):
        validators.validate_content_type(request)
        data = request.data
        teacher_id = data.get("teacher_id", "")
        subject_id = data.get("subject_id", "")
        group_id = data.get("group_id", "")
        if not teacher_id:
            msg = "teacher_id is missing"
            raise serializers.ValidationError(
                {
                    "result": False,
                    "msg": msg,
                },
                code="validation_error",
            )
        if str(teacher_id).isdigit() is False:
            msg = "teacher_id is invalid"
            raise serializers.ValidationError(
                {
                    "result": False,
                    "msg": msg,
                },
                code="validation_error",
            )
        if not group_id:
            msg = "group id is missing"
            raise serializers.ValidationError(
                {
                    "result": False,
                    "msg": msg,
                },
                code="validation_error",
            )
        if str(group_id).isdigit() is False:
            msg = "group id is invalid"
            raise serializers.ValidationError(
                {
                    "result": False,
                    "msg": msg,
                },
                code="validation_error",
            )
        if not subject_id:
            msg = "subject_id is missing"
            raise serializers.ValidationError(
                {
                    "result": False,
                    "msg": msg,
                },
                code="validation_error",
            )
        if str(subject_id).isdigit() is False:
            raise serializers.ValidationError(
                {
                    "result": False,
                    "msg": "subject id must be number",
                },
                code="validation_error",
            )
        teacher_models = models_api.TeacherModel()
        teacher_data = teacher_models.get_teacher_details_by_id(teacher_id=teacher_id)
        serializer_data = school_ops_serializers.WriteTeacherSerializer(teacher_data, data = request.data)
        if serializer_data.is_valid():
            serializer_data.save(subject_id = subject_id, group_id = group_id)
            return response.Response(
                {
                    "result": True,
                    "msg": "success",
                    "data": serializer_data.data,
                },
                status=status.HTTP_200_OK,
            )
        return response.Response(
            {
                "result": False,
                "msg": "Validation Error",
                "error": serializer_data._errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request):
        validators.validate_content_type(request)
        data = request.data
        teacher_id = data.get("teacher_id", "")
        if not teacher_id:
            msg = "teacher_id is missing"
            raise serializers.ValidationError(
                {
                    "result": False,
                    "msg": msg,
                },
                code="validation_error",
            )
        if str(teacher_id).isdigit() is False:
            raise serializers.ValidationError(
                {
                    "result": False,
                    "msg": "teacher_id must be number",
                },
                code="validation_error",
            )
        teacher_models = models_api.TeacherModel()
        teacher_data = teacher_models.get_teacher_details_by_id(teacher_id = teacher_id)
        teacher_data.is_active = False
        teacher_data.save()
        return response.Response({
            "result": True,
            "msg": "success",
            "data": {"teacher_id": teacher_id}},
            status=status.HTTP_200_OK,
        )
    
    def get(self, request):
        validators.validate_content_type(request)
        data = request.data
        teacher_id = data.get("teacher_id", "")
        if not teacher_id:
            msg = "teacher_id is missing"
            raise serializers.ValidationError(
                {
                    "result": False,
                    "msg": msg,
                },
                code="validation_error",
            )
        if str(teacher_id).isdigit() is False:
            raise serializers.ValidationError(
                {
                    "result": False,
                    "msg": "teacher_id must be number",
                },
                code="validation_error",
            )
        teacher_model = models_api.TeacherModel()
        teacher_data = teacher_model.get_teacher_details_by_id(teacher_id=teacher_id)
        print(teacher_data.values())
        serializerd_data = school_ops_serializers.TeacherSerializer(teacher_data, many=True)
        print(serializerd_data.data)
        return response.Response(
            {
                "result": True,
                "msg": "success",
                "data": serializerd_data.data,
            },
            status=status.HTTP_200_OK,
        )


class StudentsAPI(APIView):

    permission_classes = [permissions.AllowAny]
    def post(self, request):
        validators.validate_content_type(request)
        data = request.data
        first_name = data.get("first_name", "")
        group_id = data.get("group_id", "")
        last_name = data.get("last_name", "")

        if not first_name:
            msg = "first_name cannot be empty"
            raise serializers.ValidationError(
                {
                    "result": False,
                    "msg": msg,
                },
                code="validation_error",
            )
        if not group_id:
            msg = "group_id cannot be empty"
            raise serializers.ValidationError(
                {
                    "result": False,
                    "msg": msg,
                },
                code="validation_error",
            )
        if str(group_id) is True:
            msg = "group_id is in invalid format"
            raise serializers.ValidationError(
                {
                    "result": False,
                    "msg": msg,
                },
                code="validation_error",
            )
        if not last_name:
            msg = "last_name cannot be empty"
            raise serializers.ValidationError(
                {
                    "result": False,
                    "msg": msg,
                },
                code="validation_error",
            )

        serializer = school_ops_serializers.WriteStudentSerializer(
            data=request.data)
        # print("serializer", serializer)
        if not serializer.is_valid():
            return response.Response(
                {
                    "result": False,
                    "msg": "Validation error",
                    "error": serializer._errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer.check_record_if_exists(data=request.data)
        serializer.save(first_name = first_name, last_name = last_name, group_id = group_id)
        return response.Response(
            {
                "result": True,
                "msg": "success",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )
    
    def put(self, request):
        validators.validate_content_type(request)
        data = request.data
        student_id  = data.get( "student_id", "")
        first_name = data.get("first_name", "")
        last_name = data.get("last_name", "")
        group_id = data.get("group_id", "")
        if not first_name:
            msg = "first_name is missing"
            raise serializers.ValidationError(
                {
                    "result": False,
                    "msg": msg,
                },
                code="validation_error",
            )
        if not last_name:
            msg = "last_name is missing"
            raise serializers.ValidationError(
                {
                    "result": False,
                    "msg": msg,
                },
                code="validation_error",
            )
        if str(group_id).isdigit() is False:
            msg = "group_id is invalid"
            raise serializers.ValidationError(
                {
                    "result": False,
                    "msg": msg,
                },
                code="validation_error",
            )
        if not group_id:
            msg = "group id is missing"
            raise serializers.ValidationError(
                {
                    "result": False,
                    "msg": msg,
                },
                code="validation_error",
            )
        if not student_id:
            msg = "student_id is missing"
            raise serializers.ValidationError(
                {
                    "result": False,
                    "msg": msg,
                },
                code="validation_error",
            )
        student_models = models_api.StudentModel()
        student_data = student_models.get_student_details_by_id(
            student_id = student_id)
        serializer_data = school_ops_serializers.WriteStudentSerializer(student_data, data = request.data)
        if serializer_data.is_valid():
            serializer_data.save(first_name = first_name, last_name = last_name, group_id = group_id)
            return response.Response(
                {
                    "result": True,
                    "msg": "success",
                    "data": serializer_data.data,
                },
                status=status.HTTP_200_OK,
            )
        return response.Response(
            {
                "result": False,
                "msg": "Validation Error",
                "error": serializer_data._errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request):
        validators.validate_content_type(request)
        data = request.data
        student_id = data.get("student_id", "")
        if not student_id:
            msg = "student_id is missing"
            raise serializers.ValidationError(
                {
                    "result": False,
                    "msg": msg,
                },
                code="validation_error",
            )
        if str(student_id).isdigit() is False:
            raise serializers.ValidationError(
                {
                    "result": False,
                    "msg": "teacher_id must be number",
                },
                code="validation_error",
            )
        student_models = models_api.StudentModel()
        student_data = student_models.get_student_details_by_id(student_id = student_id)
        student_data.is_active = False
        student_data.save()
        return response.Response({
            "result": True,
            "msg": "success",
            "data": {"student_id": student_id}},
            status=status.HTTP_200_OK,
        )
    
    def get(self, request):
        validators.validate_content_type(request)
        data = request.data
        student_id = data.get("student_id", "")
        if not student_id:
            msg = "student_id is missing"
            raise serializers.ValidationError(
                {
                    "result": False,
                    "msg": msg,
                },
                code="validation_error",
            )
        if str(student_id).isdigit() is False:
            raise serializers.ValidationError(
                {
                    "result": False,
                    "msg": "student_id must be number",
                },
                code="validation_error",
            )
        student_model = models_api.StudentModel()
        student_model.check_student_is_active_using_student_id(student_id=student_id)
        student_data = student_model.get_student_details_by_id(student_id=student_id)
        serializerd_data = school_ops_serializers.StudentSerializer(student_data, many=True)
        return response.Response(
            {
                "result": True,
                "msg": "success",
                "data": serializerd_data.data,
            },
            status=status.HTTP_200_OK,
        )


class MarksAPI(APIView):

    permission_classes = [permissions.AllowAny]
    def post(self, request):
        validators.validate_content_type(request)
        data = request.data
        student_id = data.get("student_id", "")
        subject_id = data.get("subject_id", "")
        mark = data.get("mark", "")

        if not mark:
            msg = "mark cannot be empty"
            raise serializers.ValidationError(
                {
                    "result": False,
                    "msg": msg,
                },
                code="validation_error",
            )
        if str(mark) is True:
            msg = "mark is in invalid format"
            raise serializers.ValidationError(
                {
                    "result": False,
                    "msg": msg,
                },
                code="validation_error",
            )
        
        if not student_id:
            msg = "student_id cannot be empty"
            raise serializers.ValidationError(
                {
                    "result": False,
                    "msg": msg,
                },
                code="validation_error",
            )
        if str(student_id) is True:
            msg = "student_id is in invalid format"
            raise serializers.ValidationError(
                {
                    "result": False,
                    "msg": msg,
                },
                code="validation_error",
            )
        
        if not subject_id:
            msg = "subject_id cannot be empty"
            raise serializers.ValidationError(
                {
                    "result": False,
                    "msg": msg,
                },
                code="validation_error",
            )
        if str(subject_id) is True:
            msg = "subject_id is in invalid format"
            raise serializers.ValidationError(
                {
                    "result": False,
                    "msg": msg,
                },
                code="validation_error",
            )

        serializer = school_ops_serializers.WriteMarks(
            data=request.data)
        # print("serializer", serializer)
        if not serializer.is_valid():
            return response.Response(
                {
                    "result": False,
                    "msg": "Validation error",
                    "error": serializer._errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer.check_record_if_exists(data=request.data)
        serializer.save(student_id = student_id, subject_id = subject_id, mark = mark)
        return response.Response(
            {
                "result": True,
                "msg": "success",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )
    
    def put(self, request):
        validators.validate_content_type(request)
        data = request.data
        mark_id = data.get("mark_id", "")
        student_id  = data.get( "student_id", "")
        subject_id = data.get("subject_id", "")
        mark = data.get("mark", "")
        if not mark_id:
            msg = "mark_id is missing"
            raise serializers.ValidationError(
                {
                    "result": False,
                    "msg": msg,
                },
                code="validation_error",
            )
        if not student_id:
            msg = "student_id is missing"
            raise serializers.ValidationError(
                {
                    "result": False,
                    "msg": msg,
                },
                code="validation_error",
            )
        if str(student_id).isdigit() is False:
            msg = "student_id is invalid"
            raise serializers.ValidationError(
                {
                    "result": False,
                    "msg": msg,
                },
                code="validation_error",
            )
        if not subject_id:
            msg = "subject_id id is missing"
            raise serializers.ValidationError(
                {
                    "result": False,
                    "msg": msg,
                },
                code="validation_error",
            )
        if str(subject_id).isdigit() is False:
            msg = "subject_id is invalid"
            raise serializers.ValidationError(
                {
                    "result": False,
                    "msg": msg,
                },
                code="validation_error",
            )
        if not mark:
            msg = "mark is missing"
            raise serializers.ValidationError(
                {
                    "result": False,
                    "msg": msg,
                },
                code="validation_error",
            )
        if str(mark).isdigit() is False:
            msg = "mark is invalid"
            raise serializers.ValidationError(
                {
                    "result": False,
                    "msg": msg,
                },
                code="validation_error",
            )
        mark_models = models_api.MarkModels()
        mark_data = mark_models.get_mark_details_by_id(mark_id = mark_id)
        serializer_data = school_ops_serializers.WriteMarks(mark_data, data = request.data)
        if serializer_data.is_valid():
            serializer_data.save(student_id = student_id, subject_id = subject_id, mark = mark)
            return response.Response(
                {
                    "result": True,
                    "msg": "success",
                    "data": serializer_data.data,
                },
                status=status.HTTP_200_OK,
            )
        return response.Response(
            {
                "result": False,
                "msg": "Validation Error",
                "error": serializer_data._errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request):
        validators.validate_content_type(request)
        data = request.data
        mark_id = data.get("mark_id", "")
        if not mark_id:
            msg = "mark_id is missing"
            raise serializers.ValidationError(
                {
                    "result": False,
                    "msg": msg,
                },
                code="validation_error",
            )
        if str(mark_id).isdigit() is False:
            raise serializers.ValidationError(
                {
                    "result": False,
                    "msg": "mark_id must be number",
                },
                code="validation_error",
            )
        mark_model = models_api.MarkModels()
        mark_data = mark_model.get_mark_details_by_id(mark_id = mark_id)
        mark_data.is_active = False
        mark_data.save()
        return response.Response({
            "result": True,
            "msg": "success",
            "data": {"mark_id": mark_id}},
            status=status.HTTP_200_OK,
        )


class MarksByStudentIdAPI(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        validators.validate_content_type(request)
        data = request.data
        student_id = data.get("student_id", "")
        limit = data.get("limit", '')
        offset = data.get("offset", 0)
        if not student_id:
            msg = "student_id is missing"
            raise serializers.ValidationError(
                {
                    "result": False,
                    "msg": msg,
                },
                code="validation_error",
            )
        if str(student_id).isdigit() is False:
            raise serializers.ValidationError(
                {
                    "result": False,
                    "msg": "student_id must be number",
                },
                code="validation_error",
            )
        marks_model = models_api.MarkModels()
        marks_data = marks_model.get_mark_details_by_student_id(student_id=student_id)

        # serialized_data = school_ops_serializers.WriteMarksReadOnlySerializer(marks_data, many=True)
        paginate = custom_pagination.Pagination()
        serialized_data, next_link = paginate.get_paginated_response(
            marks_data,
            offset,
            limit,
            school_ops_serializers.WriteMarksReadOnlySerializer)
        return response.Response(
            {
                "result": True,
                "msg": "success",
                "next_link" : next_link,
                "data": serialized_data,
            },
            status=status.HTTP_200_OK,
        )


class MarksWithSubjectsByStudentIdAPI(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        validators.validate_content_type(request)
        data = request.data
        student_id = data.get("student_id", "")
        limit = data.get("limit", '')
        offset = data.get("offset", 0)
        if not student_id:
            msg = "student_id is missing"
            raise serializers.ValidationError(
                {
                    "result": False,
                    "msg": msg,
                },
                code="validation_error",
            )
        if str(student_id).isdigit() is False:
            raise serializers.ValidationError(
                {
                    "result": False,
                    "msg": "student_id must be number",
                },
                code="validation_error",
            )
        marks_model = models_api.MarkModels()
        marks_data = marks_model.get_mark_details_with_subjects_by_student_id(student_id=student_id)

        # serialized_data = school_ops_serializers.WriteMarksWithSubjectsReadOnlySerializer(marks_data, many=True)
        paginate = custom_pagination.Pagination()
        serialized_data, next_link = paginate.get_paginated_response(
            marks_data,
            offset,
            limit,
            school_ops_serializers.WriteMarksWithSubjectsReadOnlySerializer)
        return response.Response(
            {
                "result": True,
                "msg": "success",
                "next_link" : next_link,
                "data": serialized_data,
            },
            status=status.HTTP_200_OK,
        )
