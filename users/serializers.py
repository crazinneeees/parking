import json
import random
import re
from datetime import timedelta

from django.contrib.auth.hashers import make_password
from redis import Redis
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer, Serializer

from users.models import User, ParkingZone, ParkingSpot, Reservation, Payment
from users.tasks import send_message


class RegisterModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = 'username', 'email', 'password', 'phone'

    def validate_password(self, value):
        return make_password(value)

    def validate_phone(self, value):
        re.sub('\D', '', value)
        return value


class ForgotPasswordSerializer(Serializer):
    email = CharField(max_length=255, required=True)

    def validate_email(self, value):
        query = User.objects.filter(email=value)
        if not query.exists():
            raise ValidationError('User with this email does not exist')
        return value

    def send_code(self):
        redis = Redis(decode_responses=True)
        email = self.validated_data.get('email')  # ✅ исправлено
        code = random.randrange(10**5, 10**6)
        data = {'code': code, "status": "False"}
        data_str = json.dumps(data)
        redis.mset({"email": data_str})
        redis.expire("email", time=timedelta(minutes=1))
        send_message(email, f"Ваш код подтверждения: {code}")


class VerifyOTP(Serializer):
    email = CharField(max_length=255)
    code = CharField(max_length=255)

    def validate(self, attrs):
        redis = Redis(decode_responses=True)
        email = attrs.get('email')
        code = attrs.get('code')
        data_str = redis.mget("email")[0]
        if not code:
            raise ValidationError("Code expired")
        data_dict: dict = json.loads(data_str)
        verify_code = data_dict.get('code')
        if str(verify_code) != str(code):
            raise ValidationError("Kod xato")
        redis.mset({email: json.dumps({"status": "True"})})
        redis.expire("email", time=timedelta(minutes=2))
        return attrs

class ChangePasswordSerializer(Serializer):
    email = CharField(max_length=255)
    password = CharField(max_length=255)
    confirm_password = CharField(max_length=255)

    def validate_email(self, value):
        redis = Redis(decode_responses=True)
        data_str = redis.get(value)
        if not data_str:
            raise ValidationError("Kodni tasdiqlash vaqti expired")
        data_dict = json.loads(data_str)
        if data_dict.get('status') != "True":
            raise ValidationError("Oldin email tasdiqlansin")
        return value

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        if password != confirm_password:
            raise ValidationError("Parollarda xatolik")
        return attrs

    def save(self, **kwargs):
        email = self.validated_data.get('email')
        password = self.validated_data.get('password')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise ValidationError("Bunday foydalanuvchi topilmadi")
        user.set_password(password)
        user.save()



#--------------------------------parking-zone-----------------------


class CreateParkingZoneModelSerializer(ModelSerializer):
    class Meta:
        model = ParkingZone
        fields = 'name', 'address', 'coordinates', 'total_spots', 'available_spots', 'hourly_rate', 'daily_rate', 'monthly_rate'



#------------------------------parking-spots----------------------------------------------------------------------


class CreateParkingSpotModelSerializer(ModelSerializer):
    class Meta:
        model = ParkingSpot
        fields = 'spot_number', 'status', 'spot_type', 'zone'


#_------------------------------reservations------------------------------------------------------------------------
class CreateReserveModelSerializer(ModelSerializer):
    class Meta:
        model = Reservation
        fields = 'user', 'spot', 'start_time', 'end_time', 'status', 'total_amount'



#--------------------------------------------payment-----------------------------------------------------------------


class CreatePaymentModelSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = 'reservation', 'user', 'amount', 'payment_method', 'status', 'transaction_id'