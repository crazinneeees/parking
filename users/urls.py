from django.urls import path
from users.views import RegisterCreateAPIView, ForgotPasswordAPIVIEW, VerifyOTPAPIView, \
    ChangePasswordAPIView, MeAPIView, UserUpdateAPIView, UserListAPIView, UserDestroyAPIView, ZonesListAPIView, \
    ParkingZoneCreateAPIView, ZoneUpdateAPIView, ZonesDestroyAPIView, GetSpotsFromZoneListAPIView, GetTokenAPIView, \
    RefreshToken, CreateSpotCreateAPIView, GetSpotsListAPIView, AvailableSpotsListAPIView, UpdateSpotUpdateAPIView, \
    GetSpotStatusAPIView, CreateReserveCreateAPIView, GetReservationsListAPIView, GetReservationAPIView, \
    ReservationUpdateAPIView, ReservationDestroyAPIView, ReservationCheckInAPIView, ReservationCheckOutAPIView, \
    PaymentCreateAPIView, PaymentListAPIView, PaymentAPIView, PaymentRefundAPIView, RevenueReportAPIView, \
    OccupancyReportAPIView, UserActivityReportAPIView

urlpatterns = [
    # path('', hello_world),
    path('login/', GetTokenAPIView.as_view()),
    path('api/token/refresh/', RefreshToken.as_view()),
    path('register/', RegisterCreateAPIView.as_view()),
    path('forgot-password', ForgotPasswordAPIVIEW.as_view()),
    path('verify-otp', VerifyOTPAPIView.as_view()),
    path('change-password', ChangePasswordAPIView.as_view()),

    # --------------------------------profile----------------------------

    path('user-info', MeAPIView.as_view()),
    path('update-user', UserUpdateAPIView.as_view()),
    path('users-list', UserListAPIView.as_view()),
    path('delete-user/<int:pk>', UserDestroyAPIView.as_view()),

    # -------------------------------parking(zones)---------------------------

    path('create-zone', ParkingZoneCreateAPIView.as_view()),
    path('zones-list', ZonesListAPIView.as_view()),
    path('update-zone/<int:pk>', ZoneUpdateAPIView.as_view()),
    path('destroy-zone/<int:pk>', ZonesDestroyAPIView.as_view()),
    path('get-spots-from-zone/<int:pk>/spots', GetSpotsFromZoneListAPIView.as_view()),

    # ---------------------------------parking(spots)--------------------------------
    path('get-spots', GetSpotsListAPIView.as_view()),
    path('create-spot', CreateSpotCreateAPIView.as_view()),
    path('available-spots', AvailableSpotsListAPIView.as_view()),
    path('update-spot/<int:pk>', UpdateSpotUpdateAPIView.as_view()),
    path('get-spot-status/<int:pk>/status', GetSpotStatusAPIView.as_view()),

    # ------------------------------------reservations----------------------------------

    path('create-reservation', CreateReserveCreateAPIView.as_view()),
    path('get-reservations', GetReservationsListAPIView.as_view()),
    path('get-reservations-id/<int:pk>', GetReservationAPIView.as_view()),
    path('update-reservations/<int:pk>', ReservationUpdateAPIView.as_view()),
    path('delete-reservations/<int:pk>', ReservationDestroyAPIView.as_view()),
    path('api/reservations/<int:pk>/checkin/', ReservationCheckInAPIView.as_view()),
    path('api/reservations/<int:pk>/checkout/', ReservationCheckOutAPIView.as_view()),

    # ---------------------------------------------payment-------------------------------------------
    path('create-payment', PaymentCreateAPIView.as_view()),
    path('payment-list', PaymentListAPIView.as_view()),
    path('payment/<int:pk>', PaymentAPIView.as_view()),
    path('payment-refund<int:pk>', PaymentRefundAPIView.as_view()),

    # -----------------------------------------------reports--------------------------------------------

    path('api/reports/revenue/', RevenueReportAPIView.as_view()),
    path('api/reports/occupancy/', OccupancyReportAPIView.as_view()),
    path('api/reports/user-activity/', UserActivityReportAPIView.as_view()),

]
