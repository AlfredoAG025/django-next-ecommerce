from rest_framework import serializers
from django.contrib.auth.models import User

from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse

from customer_manager.models import Customer


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email", "password")
        read_only_fields = ("is_active",)


class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=False)

    class Meta:
        model = Customer
        fields = ("id", "phone", "user")

    def create(self, validated_data):
        user_data = validated_data.pop("user")

        user = User.objects.create_user(
            username=user_data["username"],
            email=user_data["email"],
            password=user_data["password"],
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            is_active=False,
        )

        customer = Customer.objects.create(user=user, **validated_data)

        self.send_confirmation_email(user)

        return customer

    def send_confirmation_email(self, user):
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        confirmation_link = reverse(
            "confirm-email", kwargs={"uidb64": uid, "token": token}
        )

        confirmation_link = f"http://127.0.0.1:8000{confirmation_link}"

        send_mail(
            subject="Django Next E-Commerce | Confirm Your Email Address",
            message=f"Please confirm your email by clicking the following link: {confirmation_link}",
            from_email="arroyo.alfredo.1pm@gmail.com",
            recipient_list=[user.email],
        )
