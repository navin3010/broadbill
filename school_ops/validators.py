from rest_framework import serializers

class ValidateGroup:
    def validate(self, request):
        data = request.data
        name = data.get("name", "")

        if not name:
            msg = "name cannot be empty"
            raise serializers.ValidationError(
                {
                    "result": False,
                    "msg": msg,
                },
                code="validation_error",
            )
        
class ValidateSubject:
    def validate(self, request):
        data = request.data
        title = data.get("title", "")

        if not title:
            msg = "subject title cannot be empty"
            raise serializers.ValidationError(
                {
                    "result": False,
                    "msg": msg,
                },
                code="validation_error",
            )
        
class ValidateTeacher:
    def validate(self, request):
        data = request.data
        group_id = data.get("group_id", "")
        subject_id = data.get("subject_id", "")

        if not group_id:
            msg = "group_id cannot be empty"
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