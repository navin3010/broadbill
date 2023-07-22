from rest_framework import serializers
from django.contrib import auth

User = auth.get_user_model()

def createUser(request, validated_data: dict, is_active=True):

    username = validated_data.get("username", "")
    email = validated_data.get("email", "")
    password = validated_data.get("password", "")

    if not username:
        raise serializers.ValidationError(
            {
                "result": False, "msg": "Userame should not be empty."
            },
            code="validation_error",
        )
    if username and User.objects.filter(
            username=username).exists():
        raise serializers.ValidationError(
            {"result": False, "msg": "Username Not Available, Already Taken."},
            code="validation_error",
        )
    if not email:
        raise serializers.ValidationError(
            {"result": False, "msg": "Email missing or empty."},
            code="validation_error",
        )
    if email and User.objects.filter(
            email=email, is_active=True).exists():
        raise serializers.ValidationError(
            {"result": False, "msg": "Email addresses must be unique."},
            code="validation_error",
        )
    if password == "":
        raise serializers.ValidationError(
            {
                "result": False,
                "msg": "Password missing or empty.",
            },
            code="validation_error",
        )
    user = User(
        username=str(username).strip(),
        email=str(email).strip(),
        is_active=is_active,
    )
    user.set_password(password)
    try:
        user.save()
    except Exception as e:
        print("The Exception during user creation", str(e))
    return user
    