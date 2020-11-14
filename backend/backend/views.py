from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions
from rest_framework.decorators import permission_classes, parser_classes, api_view
from rest_framework.parsers import MultiPartParser

import json


from .forms import RegisterForm


# @api_view(['POST'])
# @permission_classes([permissions.AllowAny])
# @parser_classes([MultiPartParser])
@csrf_exempt  # TODO
def register(request):
    if request.method == 'POST':
        user_data = json.loads(request.body)
        form = RegisterForm(user_data)


        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Creating user if it not exists
            user, created = get_user_model().objects.get_or_create(
                username=username,
                defaults={'email': email,
                          'password': password}
            )

            if not created:
                return HttpResponse('User already exists', status=409)

            # Right way to set user's password
            user.set_password(password)
            user.save()

            return HttpResponse('Registered', status=201)

        print(form.errors)

        return HttpResponse(f'Not correct field(s)\n{form.errors}', status=422)
