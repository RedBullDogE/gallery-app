import json

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework.decorators import permission_classes, parser_classes, api_view
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Picture
from .serializers import PictureDetailSerializer, PictureListSerializer
from .forms import PictureForm

# TEMP
from django.views.decorators.csrf import csrf_exempt


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def picture_list(request):
    """
    View for taking all Pictures
    """
    data = PictureListSerializer(Picture.objects.all(), many=True).data

    return JsonResponse({'data': data})


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def picture_details(request, pk):
    obj = get_object_or_404(Picture, pk=pk)
    data = PictureDetailSerializer(obj).data

    return JsonResponse({'data': data})


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def picture_change(request, pk):
    picture = get_object_or_404(Picture, pk=pk)
    body = json.loads(request.body)
    picture.description = body['description']
    picture.save()

    data = {
        'status': 'success',
        'data': PictureDetailSerializer(picture).data
    }

    return JsonResponse(data, status=200)


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
@csrf_exempt  # TODO
def picture_delete(request, pk):
    get_object_or_404(Picture, pk=pk).delete()

    data = {
        'status': 'success'
    }

    return JsonResponse(data, status=200)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
@parser_classes([MultiPartParser])
@csrf_exempt  # TODO
def picture_create(request):
    """
    View as part of CRUD. Implements Create method.
    """

    form = PictureForm(request.POST, request.FILES)

    if form.is_valid():
        data = form.cleaned_data
        user = get_object_or_404(get_user_model(), id=data['author'])

        obj = Picture.objects.create(
            author=user,
            description=data['description'],
            file=data['file']
        )

        data = {
            'status': 'success',
            'data': PictureDetailSerializer(obj).data
        }
        return JsonResponse(data, status=201)
    else:
        data = {
            'status': 'failed',
            'details': 'Not correct field(s)'
        }
        return JsonResponse(data, status=422)
