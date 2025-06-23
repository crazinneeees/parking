from http import HTTPStatus
from django.http import JsonResponse
from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.models import User, ParkingZone, Payment
from users.permissions import IsAdmin
from users.serializers import RegisterModelSerializer, ForgotPasswordSerializer, VerifyOTP, ChangePasswordSerializer, \
    CreateParkingZoneModelSerializer, CreateParkingSpotModelSerializer, CreateReserveModelSerializer, \
    CreatePaymentModelSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.timezone import localtime
from django.shortcuts import get_object_or_404
from .models import Reservation, ParkingSpot
from django.db.models import Sum, Count

# @api_view(['GET'])
# def hello_world(request):
#     return Response({'message': 'Hello, World!'})

@extend_schema(tags=['auth'])
class RegisterCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterModelSerializer

@extend_schema(tags=['auth'])
@extend_schema(request=ForgotPasswordSerializer)
class ForgotPasswordAPIVIEW(APIView):
    def post(self, request):
        data = request.data
        serializer = ForgotPasswordSerializer(data=data)
        if serializer.is_valid():
            serializer.send_code()
            return JsonResponse({"status":HTTPStatus.ACCEPTED,"message":"Tasdiqlash kodi yuborildi"})
        return JsonResponse({"status":HTTPStatus.BAD_REQUEST,"error":"Bunday email bazadan topilmadi"})


@extend_schema(tags=['auth'])
@extend_schema(request=VerifyOTP)
class VerifyOTPAPIView(APIView):
    def post(self, request):
        data = request.data
        serializer = VerifyOTP(data=data)
        if serializer.is_valid():
            return JsonResponse({"status": HTTPStatus.ACCEPTED, "message": "Muvaffaqiyatli"})
        return JsonResponse({"status": HTTPStatus.BAD_REQUEST,"message": "Tadiqlash o'tmadi" ,"error": ""})

@extend_schema(tags=['auth'],request=ChangePasswordSerializer)
class ChangePasswordAPIView(APIView):
    def post(self, request):
        data = request.data
        serializer = ChangePasswordSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"status": HTTPStatus.OK, "message":"Muvaffaqqiyatli"})

        return JsonResponse({"status": HTTPStatus.BAD_REQUEST, "message": serializer.errors})


@extend_schema(tags=['auth'])
class GetTokenAPIView(TokenObtainPairView):
    pass


@extend_schema(tags=['auth'])
class RefreshToken(TokenRefreshView):
    pass





#-------------------------------profile----------------------------------------------
@extend_schema(tags=['profile'])
class MeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = RegisterModelSerializer(request.user)
        return Response(serializer.data)

@extend_schema(tags=['profile'])
@extend_schema(request=RegisterModelSerializer)
class UserUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user  # текущий залогиненный пользователь

    # def patch(self, request):
    #     user = self.get_object()
    #     serializer = RegisterModelSerializer(user, data=request.data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response({"message": "Ma'lumotlar yangilandi", "data": serializer.data}, status=status.HTTP_200_OK)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        user = self.get_object()
        serializer = RegisterModelSerializer(user, data=request.data)  # без partial=True
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Ma'lumotlar yangilandi", "data": serializer.data}, status=HTTPStatus.OK)
        return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)


@extend_schema(tags=['profile'])
class UserListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    queryset = User.objects.all()
    serializer_class = RegisterModelSerializer

@extend_schema(tags=['profile'])
class UserDestroyAPIView(DestroyAPIView):
    queryset = User.objects.all()
    lookup_url_kwarg = 'pk'
    permission_classes = [IsAuthenticated, IsAdmin]



#-------------------------------parking----------------------

@extend_schema(tags=['zones'])
class ParkingZoneCreateAPIView(CreateAPIView):
    # permission_classes = [IsAuthenticated, IsAdmin]
    queryset = ParkingZone.objects.all()
    serializer_class = CreateParkingZoneModelSerializer


@extend_schema(tags=['zones'])
class ZonesListAPIView(ListAPIView):
    queryset = ParkingZone.objects.all()
    serializer_class = CreateParkingZoneModelSerializer

@extend_schema(tags=['zones'])
@extend_schema(request=CreateParkingZoneModelSerializer)
class ZoneUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    queryset = ParkingZone.objects.all()
    lookup_url_kwarg = 'pk'
    serializer_class = CreateParkingZoneModelSerializer

@extend_schema(tags=['zones'])
class ZonesDestroyAPIView(DestroyAPIView):
    queryset = ParkingZone.objects.all()
    permission_classes = [IsAuthenticated, IsAdmin]
    lookup_url_kwarg = 'pk'

@extend_schema(tags=['zones'])
class GetSpotsFromZoneListAPIView(ListAPIView):
    serializer_class = CreateParkingSpotModelSerializer
    def get_queryset(self):
        zone_id = self.kwargs.get('pk')
        return ParkingSpot.objects.filter(zone_id=zone_id)


#---------------------------------------------parking(spots)--------------------------


@extend_schema(tags=['spots'])
class GetSpotsListAPIView(ListAPIView):
    queryset = ParkingSpot.objects.all()
    serializer_class = CreateParkingSpotModelSerializer



@extend_schema(tags=['spots'])
class CreateSpotCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = CreateParkingSpotModelSerializer
    queryset = ParkingSpot.objects.all()


@extend_schema(tags=['spots'])
class AvailableSpotsListAPIView(ListAPIView):
    serializer_class = CreateParkingSpotModelSerializer

    def get_queryset(self):
        return ParkingSpot.objects.filter(status='available')



@extend_schema(tags=['spots'])
class UpdateSpotUpdateAPIView(UpdateAPIView):
    # permission_classes = [IsAuthenticated, IsAdmin]
    queryset = ParkingSpot.objects.all()
    lookup_url_kwarg = 'pk'
    serializer_class = CreateParkingSpotModelSerializer

@extend_schema(tags=['spots'])
class GetSpotStatusAPIView(APIView):
    def get(self, request, pk):
        spot = ParkingSpot.objects.get(pk=pk)
        return Response({"status": spot.status})


#---------------------------------------------reservations-----------------------------------------

@extend_schema(tags=['reservation'])
class CreateReserveCreateAPIView(CreateAPIView):
    # permission_classes = [IsAuthenticated, IsAdmin]
    queryset = Reservation.objects.all()
    serializer_class = CreateReserveModelSerializer

@extend_schema(tags=['reservation'])
class GetReservationsListAPIView(ListAPIView):
    queryset = Reservation.objects.all()
    serializer_class = CreateReserveModelSerializer


@extend_schema(tags=['reservation'])
class GetReservationAPIView(ListAPIView):
    queryset = Reservation.objects.all()
    lookup_url_kwarg = 'pk'
    serializer_class = CreateReserveModelSerializer

@extend_schema(tags=['reservation'])
class ReservationUpdateAPIView(UpdateAPIView):
    serializer_class = CreateReserveModelSerializer
    # permission_classes = [IsAuthenticated, IsAdmin]
    queryset = Reservation.objects.all()
    lookup_url_kwarg = 'pk'


@extend_schema(tags=['reservation'])
class ReservationDestroyAPIView(DestroyAPIView):
    queryset = Reservation.objects.all()
    # permission_classes = [IsAuthenticated, IsAdmin]
    pk_url_kwarg = 'pk'


@extend_schema(tags=['reservation'])
class ReservationCheckInAPIView(APIView):
    def post(self, request, pk):
        reservation = get_object_or_404(Reservation, pk=pk)

        if reservation.status != 'active':
            return Response({'error': 'Reservation is not active.'}, status=status.HTTP_400_BAD_REQUEST)

        current_time = localtime()
        # if not (reservation.start_time <= current_time <= reservation.end_time):
        #     return Response({'error': 'Check-in time is outside reservation period.'}, status=400)

        # Занимаем место
        spot = reservation.spot
        spot.status = 'occupied'
        spot.save()

        # (Опционально) логируем время
        # reservation.checked_in_at = current_time
        reservation.save()

        return Response({'message': 'Checked in successfully.'}, status=status.HTTP_200_OK)



@extend_schema(tags=['reservation'])
class ReservationCheckOutAPIView(APIView):
    def post(self, request, pk):
        reservation = get_object_or_404(Reservation, pk=pk)

        if reservation.status != 'active':
            return Response({'error': 'Reservation is not active.'}, status=status.HTTP_400_BAD_REQUEST)

        # Освобождаем место
        spot = reservation.spot
        spot.status = 'available'
        spot.save()

        # Обновляем бронь
        reservation.status = 'completed'
        reservation.save()

        return Response({'message': 'Checked out successfully.'}, status=status.HTTP_200_OK)


#---------------------------------------------------payment----------------------------
@extend_schema(tags=['payment'])
class PaymentCreateAPIView(CreateAPIView):
    serializer_class = CreatePaymentModelSerializer
    queryset = Payment.objects.all()
    # permission_classes = [IsAuthenticated, IsAdmin]

@extend_schema(tags=['payment'])
class PaymentListAPIView(ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = CreatePaymentModelSerializer


@extend_schema(tags=['payment'])
class PaymentAPIView(ListAPIView):
    pk_url_kwarg = 'pk'
    queryset = Payment.objects.all()
    serializer_class = CreatePaymentModelSerializer

@extend_schema(tags=['payment'])
class PaymentRefundAPIView(APIView):
    # permission_classes = [IsAdmin]

    def post(self, request, pk):
        payment = get_object_or_404(Payment, pk=pk)

        if payment.status != 'completed':
            return Response({'error': 'Cannot refund a non-completed payment.'}, status=400)

        # Проверка на повторный возврат
        if payment.status == 'refunded':
            return Response({'error': 'Payment already refunded.'}, status=400)

        # Обновляем статус
        payment.status = 'refunded'
        payment.save()

        return Response({'message': 'Refund successful.'}, status=200)



#----------------------------------------------------------------------reports---------------------------------
@extend_schema(tags=['reports'])
class RevenueReportAPIView(APIView):
    # permission_classes = [IsAdmin]

    def get(self, request):
        total_revenue = Payment.objects.filter(status='completed').aggregate(Sum('amount'))['amount__sum'] or 0
        return Response({'total_revenue': total_revenue})

@extend_schema(tags=['reports'])
class OccupancyReportAPIView(APIView):
    # permission_classes = [IsAdmin, IsAuthenticated]

    def get(self, request):
        total_spots = ParkingSpot.objects.count()
        occupied_spots = ParkingSpot.objects.filter(status='occupied').count()
        available_spots = ParkingSpot.objects.filter(status='available').count()

        return Response({
            'total_spots': total_spots,
            'occupied_spots': occupied_spots,
            'available_spots': available_spots,
            'occupancy_rate_percent': round((occupied_spots / total_spots) * 100, 2) if total_spots else 0
        })

@extend_schema(tags=['reports'])
class UserActivityReportAPIView(APIView):
    # permission_classes = [IsAdmin]

    def get(self, request):
        activity = User.objects.annotate(reservation_count=Count('reservations')).values('id', 'username', 'reservation_count')
        return Response(list(activity))