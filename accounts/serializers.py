from rest_framework import serializers
from .models import Student
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    city = serializers.CharField(required=True)
    major = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = Student
        fields = ['fullname', 'phone_number', 'email', 'city', 'major', 'password']

    # ✅ Handle duplicate phone numbers before hitting the DB
    def validate_phone_number(self, value):
        if Student.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("This phone number is already registered.")
        return value

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        student = super().create(validated_data)
        return student

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            "user": {
                "id": instance.id,
                "fullname": instance.fullname,
                "phone_number": instance.phone_number,
                "email": instance.email,
                "city": instance.city,
                "major": instance.major,
            },
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        }


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})

    def validate(self, attrs):
        phone_number = attrs.get("phone_number")
        password = attrs.get("password")

        try:
            student = Student.objects.get(phone_number=phone_number)
        except Student.DoesNotExist:
            raise serializers.ValidationError({"phone_number": "No account found with this phone number."})

        if not student.check_password(password):
            raise serializers.ValidationError({"password": "Incorrect password."})

        refresh = RefreshToken.for_user(student)

        return {
            "user": {
                "id": student.id,
                "fullname": student.fullname,
                "phone_number": student.phone_number,
                "email": student.email,
                "city": student.city,
                "major": student.major,
            },
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        }
