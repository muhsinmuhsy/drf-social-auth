from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from auth_app.serializers import *
from rest_framework.response import Response
from rest_framework import status
from auth_app.utils import send_code_to_user
from auth_app.models import *
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class RegisterUserView(GenericAPIView):
    serializer_class = UserRegisterSerializer
    
    def post(self, request):
        user_data = request.data
        serializer = self.serializer_class(data=user_data)
        # if serializer.is_valid(raise_exception=True):
        #     serializer.save()
        #     user = serializer.data
        #     send_code_to_user(user['email'])
        #     #send email function user ['email']
        #     return Response({
        #         'data': user,
        #         'message': f'Hi {user.first_name}, thanks for signing up a passcode has be send .'
        #     }, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user_data = serializer.data  # user_data is a dictionary
            send_code_to_user(user_data['email'])
            # send email function using user_data['email']
            return Response({
                'data': user_data,
                'message': f"Hi {user_data['first_name']}, thanks for signing up. A passcode has been sent."
            }, status=status.HTTP_201_CREATED)


class VerifyUserEmail(GenericAPIView):
    serializer_class = VerifyUserEmailSerializer
    
    def post(self, request):
        otpcode = request.data.get('otp')
        try:
            user_code_obj = OneTimePassword.objects.get(code=otpcode)
            user = user_code_obj.user
            if not user.is_verified:
                user.is_verified=True
                user.save()
                return Response({
                    'message' : 'account email verified successfully'
                }, status=status.HTTP_200_OK)
            return Response({
                'message' : "code is invalid user already verified"
            }, status=status.HTTP_204_NO_CONTENT)
        
        except OneTimePassword.DoesNotExist:
            return Response({'message':'passcode not provided'}, status=status.HTTP_404_NOT_FOUND)
        

class LoginUserView(GenericAPIView):
    serializer_class = LoginSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class TestAuthenticationView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        data = {
            'msg':'its works'
        }
        return Response(data, status=status.HTTP_200_OK)