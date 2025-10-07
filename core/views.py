
from django.shortcuts import render
from .models import user
from .serializers import userSerializers
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import logout

import random
from django.core.mail import send_mail

# Create your views here.
otp_storage = {}

@api_view(["POST"])
def register(request):
    try:
        First_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        email = request.data.get("email")
        phone = request.data.get("phone")
        password = request.data.get("password")
        otp = request.data.get("otp")
    

        usercreate = user.objects.create(
            First_name= First_name,
            last_name=last_name,
            email=email,
            phone =phone,
            password=password,
            otp =otp
        

        )

        
        otp = str(random.randint(100000, 999999))
        otp_storage[email] = otp

        send_mail(
            subject="Your OTP Code",
            message=f"Your OTP is: {otp}",
            from_email="noreply@example.com",
            recipient_list=[email],
            fail_silently=False,
        )

        usercreate.save()

        if not send_mail:
            return Response({"msg":"mail not send"},status=400)

        if not First_name or not last_name or not email or not password:
            return Response({"message":"all fields required"},status=400)
        

        if len(password) < 8:
            return Response({"message":"password must be at least 8 characters"},status=400)
            

        return Response({"message":"register create successfully"},status=200)
    
    except Exception as e:
        return Response({"message":"register created as str:{e}"},status=500)
    

@api_view(['POST'])
def login_user(request):
     try:
        email =request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response({"msg":"email and password  are required"},status=400)
        try:
            user_login = user.objects.get(
                email=email,
                password=password
            )
        except user.DoesNotExist:
            return Response({"msg":"invalid credentials"},status =400)    
        return Response({"msg":"user login successfully"},status=200)
     
     except Exception as e:
         return Response({"msg":"login created {str:{e}}"},status =400)




@api_view(['POST'])
def verify_otp(request):
    email = request.data.get("email")
    otp = request.data.get("otp")

    if not email or not otp:
        return Response({"message":"all fields or reqiured"},status=400)
    if otp_storage.get(email) == otp:
        return Response({"message":"otp verified successfully"},status=200)
    else:
        return Response({"message":"invalid otp "},status=400)


@api_view(['POST'])
def logout_view(request):
    logout(request._request)
    if not logout:
        return Response({"logout not done"},status=400)
    else:
        return Response({"msg":"logout successfully"},status=200)


@api_view(['POST'])
def user_profile(request):
    profile_picture = request.FILES.get("profile_picture")
    first_name = request.data.get("First_name")
    last_name = request.data.get("last_name")
    email = request.data.get("email")
    phone = request.data.get("phone")
    password = request.data.get("password")
    try:
        user_profile = user.objects.get(email=email)
    except user.DoesNotExist:
        return Response({"msg":"user not found"},status=404)
    if profile_picture:
        user_profile.profile_picture = profile_picture
    if first_name:
        user_profile.First_name = first_name
    if last_name:
        user_profile.last_name = last_name
    if phone:
        user_profile.phone = phone
    if password:
        user_profile.password = password
    user_profile.save()
    serializer = userSerializers(user_profile)
    return Response(serializer.data, status=200)

@api_view(['GET'])
def user_details(request):
    users = user.objects.all()
    serializer = userSerializers(users, many=True)
    return Response(serializer.data, status=200)

@api_view(['PUT'])
def user_update(request, email):
    try:
        user_update = user.objects.get(email=email)
    except user.DoesNotExist:
        return Response({"msg":"user not found"},status=404)
    profile_picture = request.FILES.get("profile_picture")
    first_name = request.data.get("First_name")
    last_name = request.data.get("last_name")
    phone = request.data.get("phone")
    password = request.data.get("password")
    if profile_picture:
        user_update.profile_picture = profile_picture
    if first_name:
        user_update.First_name = first_name
    if last_name:
        user_update.last_name = last_name
    if phone:
        user_update.phone = phone
    if password:
        user_update.password = password
    user_update.save()
    serializer = userSerializers(user_update)
    return Response(serializer.data, status=200)


@api_view(['DELETE'])
def user_delete(request, email):
    try:
        user_delete = user.objects.get(email=email)
    except user.DoesNotExist:
        return Response({"msg":"user not found"},status=404)
    user_delete.delete()
    return Response({"msg":"user deleted successfully"}, status=200)