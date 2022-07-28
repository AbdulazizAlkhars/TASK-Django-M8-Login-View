import datetime
from rest_framework import generics
from flights import serializers
from flights.models import Booking, Flight


class FlightsList(generics.ListAPIView):
    queryset = Flight.objects.all()
    serializer_class = serializers.FlightSerializer


class BookingsList(generics.ListAPIView):
    serializer_class = serializers.BookingSerializer

    def get_queryset(self):
        return Booking.objects.filter(date__gte=datetime.date.today())


class BookingDetails(generics.RetrieveAPIView):
    queryset = Booking.objects.all()
    serializer_class = serializers.BookingDetailsSerializer
    lookup_url_kwarg = "booking_id"


class UpdateBooking(generics.RetrieveUpdateAPIView):
    queryset = Booking.objects.all()
    serializer_class = serializers.UpdateBookingSerializer
    lookup_url_kwarg = "booking_id"


class CancelBooking(generics.DestroyAPIView):
    queryset = Booking.objects.all()
    lookup_url_kwarg = "booking_id"


class UserRegistration(generics.CreateAPIView):
    serializer_class = serializers.UserRegistrationSerializer


class LoginUserViwe():
    pass


"""
Create a Booking create API view:
It should use the same serializer as the update view.
The flight should get assigned automatically to the booking. The flight id should be retrieved from the url.
The user should get assigned automatically to the booking. The logged in user who is creating the booking should get assigned as the user.
"""


class CreateBooking(generics.CreateAPIView):
    serializer_class = serializers.UpdateBookingSerializer
    # queryset = Booking.objects.all()

    def perform_create(self, serializer):
        print("!!!!!!!!!!!!", self.request.user)
        serializer.save(flight=Flight.objects.get(
            id=self.kwargs["flight_id"]), user=self.request.user)
        # return serializer.data
