from rest_framework import serializers
from martin_deliver.delivery.models import Courier, Collection, Package
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
import django.contrib.auth.password_validation as validators
from django.core import exceptions
from rest_framework_simplejwt.tokens import RefreshToken
import random
import string
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework.fields import CurrentUserDefault

def random_username():
    return "".join(
        random.SystemRandom().choice(
            string.ascii_lowercase + string.digits + string.ascii_uppercase
        )
        for _ in range(12)
    )

def get_user(self):
    user = None
    request = self.context.get("request")
    if request and hasattr(request, "user"):
        user = request.user
    return user

########### EMAIL AUTH WITH JWT ################

class EmailTokenObtainSerializer(TokenObtainSerializer):
    username_field = User.EMAIL_FIELD

class CustomTokenObtainPairSerializer(EmailTokenObtainSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        return data

class CourierSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text="should not be a common password, can't be only numbers, should be at least 8 characters.",
        style={"input_type": "password", "placeholder": "Password"},
    )
    token = serializers.SerializerMethodField()
    username = serializers.CharField(
        write_only=True, required=False, help_text="random generated username"
    )

    class Meta:
        model = Courier
        fields = (
            "phone_number",
            "email",
            "first_name",
            "last_name",
            "password",
            "token",
            "username",
        )
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
            "email": {"required": True},
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
        validated_data["username"] = random_username()
        validated_data["password"] = make_password(validated_data.get("password"))
        return super(CourierSignupSerializer, self).create(validated_data)

    def get_token(self, user):
        tokens = RefreshToken.for_user(user)
        refresh = str(tokens)
        access = str(tokens.access_token)
        data = {"refresh": refresh, "access": access}
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
    token = serializers.SerializerMethodField()
    username = serializers.CharField(
        write_only=True, required=False, help_text="random generated username"
    )

    class Meta:
        model = Collection
        fields = ("email", "password", "name", "webhook_link", "token", "username")

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
        validated_data["username"] = random_username()
        validated_data["password"] = make_password(validated_data.get("password"))
        return super(CollectionSignupSerializer, self).create(validated_data)

    def get_token(self, user):
        tokens = RefreshToken.for_user(user)
        refresh = str(tokens)
        access = str(tokens.access_token)
        data = {"refresh": refresh, "access": access}
        return data


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ("email", "name", "webhook_link")


class PackageCreateSerializer(serializers.ModelSerializer):
    sender = CollectionSerializer(required=False)
    class Meta:
        model=Package
        fields = (
            "sender_phone_number",
            "sender_name",
            "receiver_phone_number",
            "receiver_name",
            "origin_long",
            "origin_lat",
            "origin_address",
            "destination_long",
            "destination_lat",
            "destination_address",
            "slug",
            "sender",
        )

    def create(self, validated_data):
        validated_data["sender"] = Collection.objects.get(email=get_user(self).email)
        return super(PackageCreateSerializer, self).create(validated_data)

