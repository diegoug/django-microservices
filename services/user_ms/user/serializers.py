
from datetime import datetime

from django.contrib.auth import password_validation, authenticate
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from oauth2_provider.models import Application, AccessToken

from profiles.models import User


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']


class UserUpdateModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','first_name','last_name']


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        min_length=8, max_length=64)

    def validate(self, data): # TODO:review
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError('The credentials are not valid')

        self.context['user'] = user
        return data

    def create(self, data):
        # http://tutorials.jenkov.com/oauth2/client-types.html
        oauth_data = {
            'authorization_grant_type': 'client-credentials',
            "client_type": "confidential",
            'user': self.context['user']
        }

        if not Application.objects.filter(**oauth_data).exists():
            oauth_application = Application(**oauth_data)
            oauth_application.save()

        oauth2_app = Application.objects.get(**oauth_data)

        return self.context['user'], \
               oauth2_app.authorization_grant_type.replace('-','_'), \
               oauth2_app.client_secret, oauth2_app.client_id


class UserSignUpSerializer(serializers.Serializer):
    username = serializers.CharField(
        min_length=4,
        max_length=20,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    first_name = serializers.CharField(
        min_length=2, max_length=50)
    last_name = serializers.CharField(
        min_length=2, max_length=100)

    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(
        min_length=8, max_length=64)
    password_confirmation = serializers.CharField(
        min_length=8, max_length=64)

    def validate(self, data):
        passwd = data['password']
        passwd_conf = data['password_confirmation']
        if passwd != passwd_conf:
            raise serializers.ValidationError('Passwords do not match')
        password_validation.validate_password(passwd)

        return data

    def create(self, data):
        data.pop('password_confirmation')
        user = User.objects.create_user(**data)
        content_type = ContentType.objects.get_for_model(user)
        permission = Permission.objects.get(
            codename="add_user", content_type=content_type
        )
        user.user_permissions.add(permission)
        permission = Permission.objects.get(
            codename="change_user", content_type=content_type
        )
        user.user_permissions.add(permission)
        permission = Permission.objects.get(
            codename="delete_user", content_type=content_type
        )
        user.user_permissions.add(permission)
        return user


class UserGetOAuthCredentials(serializers.Serializer):

    def validate(self, data):
        if self.context['request'].user.is_anonymous:
            raise serializers.ValidationError('This user have not credentials')
        return data

    def create(self, data):
        oauth_data = {
            'authorization_grant_type': 'client-credentials',
            "client_type": "confidential",
            'user': self.context['request'].user
        }

        if not Application.objects.filter(**oauth_data).exists():
            oauth_application = Application(**oauth_data)
            oauth_application.save()

        oauth2_app = Application.objects.get(**oauth_data)

        return oauth2_app.authorization_grant_type.replace('-','_'), \
               oauth2_app.client_secret, oauth2_app.client_id


class UserGetOAuthToken(serializers.Serializer):
    client_secret = serializers.CharField(max_length=255)
    client_id = serializers.CharField(max_length=100)

    def validate(self, data):
        if self.context['request'].user.is_anonymous:
            raise serializers.ValidationError('Invalid user')
        return data

    def create(self, data):
        data_model = {
            'application__client_secret': data['client_secret'],
            'application__client_id': data['client_id'],
            'expires__gte': datetime.now()
        }

        access_token = {}

        access_token_object = AccessToken.objects.filter(**data_model)

        if access_token_object.exists():
            access_token = access_token_object.first().token

        return access_token
