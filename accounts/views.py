from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .serializers import RegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        student = serializer.save()

        # generate JWT tokens
        refresh = RefreshToken.for_user(student)
        access_token = str(refresh.access_token)

        # build response
        data = {
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
                "access": access_token,
            }
        }
        return Response(data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoginSerializer


@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
