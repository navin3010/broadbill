from rest_framework import serializers

def validate_content_type(request):
    content_type = request.content_type
    if str(content_type) != "application/json":
        raise serializers.ValidationError(
            {"result": False, "msg": "Invalid content type or missing"},
            code="validation_error",
        )