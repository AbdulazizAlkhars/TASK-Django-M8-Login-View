from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Booking, Flight
from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = ["destination", "time", "price", "id"]


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["flight", "date", "id"]


class BookingDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["flight", "date", "passengers", "id"]


class UpdateBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["date", "passengers"]


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["username", "password"]

        def create(self, validated_data):
            password = validated_data.pop("password")
            new_user = User(**validated_data)
            new_user.set_password(password)
            return validated_data


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    access = serializers.CharField(read_only=True, allow_blank=True)

    def validate(self, data):
        my_username = data.get("username")
        my_password = data.get("password")

        try:
            user = User.objects.get(username=my_username)
        except user.DoesNotExist:
            raise serializers.ValidationError("User does not exist")

        if not user.check_password(my_password):
            raise serializers.ValidationError("Incorrect password")

        payload = RefreshToken.for_user(user)
        token = str(payload.access_token)
        data["access"] = token

        return data
