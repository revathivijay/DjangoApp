import datetime
from datetime import datetime

from django.contrib.auth import user_logged_in
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework_jwt.settings import api_settings

import validators  # for validating URL (can be replaced with regex check if needed)
from nurtureLabsDjangoApp.models import User, Advisor, Booking
from nurtuteLabsDjango import settings
import json
import jwt
import base64

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


# TODO: hash passwords while saving in database

def home(request):
    return HttpResponse('This is Home')


def admin(request):
    return HttpResponse('This is Admin')


@csrf_exempt
@api_view(['POST'])
def insert_advisor(request):
    try:
        advisor_name = request.POST.get('name')
        advisor_photo_url = request.POST.get('photo_url')
        if not validators.url(advisor_photo_url):  # if invalid URL, reset it to None
            advisor_photo_url = None

        # enter values into database
        advisor = Advisor(name=advisor_name, photo_url=advisor_photo_url)
        advisor.save()
        return HttpResponse(status=status.HTTP_200_OK)  # all parameters received, OK

    except KeyError:
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def user_register(request):
    try:
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User(name=name, email=email, password=password)
        print(user)
        user.save()

        payload = jwt_payload_handler(user)
        token = jwt.encode(payload, settings.SECRET_KEY)

        user_details = {'user_id': user.user_id, 'token': token.decode('ascii')}

        return HttpResponse(json.dumps(user_details), content_type='application/json', status=status.HTTP_200_OK)  # OK

    except KeyError:
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def user_login(request):
    try:
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.filter(email=email, password=password).values("user_id")[0]
        print(user)

        if user:
            payload = jwt_payload_handler(user)
            token = jwt.encode(payload, settings.SECRET_KEY)
            user_details = {'token': token.decode('ascii'), 'user_id': user['user_id']}

            user_logged_in.send(sender=user.__class__,
                                request=request, user=user)
            return HttpResponse(json.dumps(user_details), content_type='application/json',
                                status=status.HTTP_200_OK)

        else:  # no matching user
            return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)

    except KeyError:
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_advisor_list(request, user_id):
    advisors = Advisor.objects.values()
    advisors = list(advisors)
    print(advisors)
    response_data = {'advisor_list': advisors,
                     'status': status.HTTP_200_OK,
                     }
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@api_view(['POST'])
def book_call_with_advisor(request, user_id, advisor_id):
    date_time = request.POST.get('datetime')

    # convert string to datetime object
    date_time_obj = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')

    # extract date and time
    date = datetime.strftime(date_time_obj, '%Y-%m-%d')
    time = datetime.strftime(date_time_obj, '%H:%M:%S')
    print(date, " ", time)

    advisor = Advisor.objects.filter(id=advisor_id)
    booking = Booking(advisor_id, user_id=user_id, date=date, time=time)
    booking.save()
    return HttpResponse(status=status.HTTP_200_OK)


@api_view(['GET'])
def get_booking_list(request, user_id):
    bookings = Booking.objects.filter(user_id=user_id).values()
    bookings = list(bookings)

    # getting advisor details and converting datetime object to string
    for i in range(len(bookings)):
        advisor = Advisor.objects.filter(id=bookings[i]['id_id']).values("id", "name", "photo_url")[0]
        bookings[i]['advisor_id'] = advisor['id']
        bookings[i]['advisor_name'] = advisor['name']
        bookings[i]['advisor_photo'] = advisor['photo_url']
        bookings[i]['date'] = bookings[i]['date'].strftime("%Y-%m-%d")
        bookings[i]['time'] = bookings[i]['time'].strftime("%H:%M:%S")

        del bookings[i]['id_id']
        del bookings[i]['user_id']

    response_body = {
        'booking_list': bookings,
        'status': status.HTTP_200_OK
    }
    return HttpResponse(json.dumps(response_body), content_type='application/json')
