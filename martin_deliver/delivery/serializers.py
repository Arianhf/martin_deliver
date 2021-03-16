from rest_framework import serializers
from martin_deliver.delivery.models import Courier, Collection
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
import django.contrib.auth.password_validation as validators
from django.core import exceptions
from rest_framework_simplejwt.tokens import RefreshToken
import random
import string

class CourierSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text="should not be a common password, can't be only numbers, should be at least 8 characters.",
        style={"input_type": "password", "placeholder": "Password"},
    )
    token = serializers.SerializerMethodField()

    class Meta:
        model = Courier
        fields = (
            "phone_number",
            "email",
            "first_name",
            "last_name",
            "password",
            "token"
        )
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True}
        }

    def validate_password(self, data):
        # get the password from the data
        password = data

        errors = dict()
        try:
            # validate the password and catch the exception
            validators.validate_password(password=password)

        # the exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
            errors = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return password

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError(_("Email can't be blank!"))
        email = value

        try:
            user_email = self.user.email
        except:
            user_email = None

        if User.objects.filter(email__iexact=email):
            raise serializers.ValidationError(_("Email is already in use!"))
        return email

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data.get("password"))
        return super(CourierSignupSerializer, self).create(validated_data)

    def get_token(self, user):
        tokens = RefreshToken.for_user(user)
        refresh = str(tokens)
        access = str(tokens.access_token)
        data = {
            "refresh": refresh,
            "access": access
        }
        return data

class CourierSerializer(serializers.ModelSerializer):

    class Meta:
        model = Courier
        fields = (
            "phone_number",
            "email",
            "first_name",
            "last_name",
        )


class CollectionSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text="should not be a common password, can't be only numbers, should be at least 8 characters.",
        style={"input_type": "password", "placeholder": "Password"},
    )
    username = serializers.CharField(
        write_only=True, required=False, help_text="random generated username"
    )
    token = serializers.SerializerMethodField()

    class Meta:
        model = Collection
        fields = (
            "phone_number",
            "email",
            "password",
            "name",
            "webhook_link",
        )

    def validate_password(self, data):
        # get the password from the data
        password = data

        errors = dict()
        try:
            # validate the password and catch the exception
            validators.validate_password(password=password)

        # the exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
            errors = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return password

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError(_("Email can't be blank!"))
        email = value

        try:
            user_email = self.user.email
        except:
            user_email = None

        if User.objects.filter(email__iexact=email):
            raise serializers.ValidationError(_("Email is already in use!"))
        return email

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data.get("password"))
        return super(CollectionSignupSerializer, self).create(validated_data)

    def get_token(self, user):
        tokens = RefreshToken.for_user(user)
        refresh = str(tokens)
        access = str(tokens.access_token)
        data = {
            "refresh": refresh,
            "access": access
        }
        return data

class CollectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Collection
        fields = (
            "phone_number",
            "email",
            "name",
            "webhook"
        )