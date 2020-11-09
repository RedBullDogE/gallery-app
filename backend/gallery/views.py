import json

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework.decorators import permission_classes, parser_classes, api_view
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.paginator import Paginator

from .models import Picture
from .serializers import PictureDetailSerializer, PictureListSerializer
from .forms import PictureForm

# TEMP
from django.views.decorators.csrf import csrf_exempt


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
@parser_classes([MultiPartParser])
@csrf_exempt  # TODO
def picture_create(request):
    """
    View for adding new pictures
    Part of CRUD implementation (CREATE)
    """
    form = PictureForm(request.POST, request.FILES)

    if form.is_valid():
        data = form.cleaned_data
        user = get_object_or_404(get_user_model(), id=request.user.id)

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


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def picture_list(request):
    """
    View for taking all Pictures.
    Part of CRUD implementation (READ | list)
    """
    paginator = Paginator(Picture.objects.all(), 2)
    page = request.GET.get('page') or 1

    picture_page = paginator.get_page(page)

    data = {
        "page": picture_page.number,
        "pageCount": picture_page.paginator.num_pages,
        "data": PictureListSerializer(picture_page, many=True).data
    }

    return JsonResponse(data, status=200)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def picture_details(request, pk):
    """
    View for taking details of the specified picture 
    Part of CRUD implementation (READ | details)
    """
    obj = get_object_or_404(Picture, pk=pk)
    data = PictureDetailSerializer(obj).data

    return JsonResponse({'data': data}, status=200)


# TODO: to patch?
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def picture_change(request, pk):
    """
    View for changing of the specified picture details
    Part of CRUD implementation (UPDATE)
    """
    picture = get_object_or_404(Picture, pk=pk)

    if picture.author != request.user:
        data = {
            'status': 'failed',
            'details': 'Not allowed'
        }
        return JsonResponse(data, status=403)

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
    """
    View for deleting of the specified picture
    Part of CRUD implementation (DELETE)
    """
    picture = get_object_or_404(Picture, pk=pk)

    if picture.author != request.user:
        data = {
            'status': 'failed',
            'details': 'Not allowed'
        }
        return JsonResponse(data, status=403)

    data = {
        'status': 'success',
        'data': PictureDetailSerializer(picture).data
    }
    picture.delete()

    return JsonResponse(data, status=200)
