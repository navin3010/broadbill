from django.shortcuts import render
from rest_framework import response, decorators, permissions, status, serializers
from django.contrib import auth
from .import validators, models, serializers as user_serializers
from techmos import settings
import jwt
from django.contrib.auth.signals import user_logged_in

User = auth.get_user_model()

@decorators.api_view(["POST"])
@decorators.permission_classes([permissions.AllowAny])
def signup(request):
    validators.validate_content_type(request)

    user = serializers.createUser(
        request, validated_data=request.data,
        is_active=True)
    msg = "Success"
    res = {
        "result": True,
        "msg": msg,
        "data": {
            "user_id": user.id,
            "email": user.email,
            "username": user.username,
        }
    }
    return response.Response(res, status=status.HTTP_201_CREATED)

@decorators.api_view(["POST"])
@decorators.permission_classes([permissions.AllowAny])
def GetToken(request):

    def jwt_payload_handler(user):
        return {
            'user_id': user.pk,
            'email': user.email,
            # 'is_superuser': user.is_superuser,
            # 'exp': datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA,
            # 'orig_iat': timegm(
            #     datetime.utcnow().utctimetuple()
            # )
        }

    validators.validate_content_type(request)
    try:
        # print("try view")
        # username = request.data['username']
        email = request.data['email']
        password = request.data['password']
        print("username", email)
        if not email:
            raise serializers.ValidationError(
                {
                    "result": False, "msg": "email should not be empty."
                },
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
        # user = User.objects.get(email=email, password=password)
        print("55")
        try:
            user = User.objects.get(username = email)
        except Exception as e:
            raise serializers.ValidationError(
                {
                    "result": False,
                    "msg": "User does not exists please check username or password",
                },
                code="validation_error",
            )
        print("data", user)
        if not user.check_password(password):
            raise serializers.ValidationError({
                "result": False,
                "msg": "Invalid Username or Password, Please Sign up again"},
                code="validation_error",
            )
        print("64")
        if user:
            try:
                payload = jwt_payload_handler(user)
                token = jwt.encode(payload, settings.SECRET_KEY)
                user_details = {}
                # user_details['name'] = "%s %s" % (
                #     user.first_name, user.last_name)
                user_details["name"] = user.username
                user_details['token'] = token
                user_logged_in.send(sender=user.__class__,
                                    request=request, user=user)
                return response.Response(user_details, status=status.HTTP_200_OK)
            except Exception as e:
                raise e
        else:
            res = {
                'error': 'can not authenticate with the given credentials or the account has been deactivated'
                }
            return response.Response(res, status=status.HTTP_403_FORBIDDEN)
    except KeyError:
        res = {
            'error': 'please provide a email and a password'
            }
        return response.Response(res)