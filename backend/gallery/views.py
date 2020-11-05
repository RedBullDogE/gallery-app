from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse

from .models import Picture
from .serializers import PictureDetailSerializer, PictureListSerializer
from .forms import PictureForm
from django.contrib.auth import get_user_model

from django.views.decorators.csrf import csrf_exempt


def picture_list(request):
    """
    View for taking all Pictures
    """
    if request.method == 'GET':
        data = PictureListSerializer(Picture.objects.all(), many=True).data

        return JsonResponse({'data': data})
    else:
        return HttpResponse('Method is not allowed', status=405)


@csrf_exempt  # TODO
def picture(request, pk):
    """
    View as part of CRUD. Implements Reading, Updating and Deleting methods.
    """
    if request.method == 'GET':
        obj = get_object_or_404(Picture, pk=pk)
        data = PictureDetailSerializer(obj).data

        return JsonResponse({'data': data})
    elif request.method == 'POST':
        picture = get_object_or_404(Picture, pk=pk)
        picture.description = request.POST.get('description')
        picture.save()

        return HttpResponse('Chenged', status=200)
    elif request.method == 'DELETE':
        get_object_or_404(Picture, pk=pk).delete()

        return HttpResponse('Deleted', status=200)
    else:
        return HttpResponse('Method is not allowed', status=405)


@csrf_exempt  # TODO
def create_picture(request):
    """
    View as part of CRUD. Implements Create method.
    """
    if request.method == 'POST':
        form = PictureForm(request.POST, request.FILES)

        if form.is_valid():
            data = form.cleaned_data
            user = get_object_or_404(get_user_model(), id=data['author'])

            Picture.objects.create(
                author=user,
                description=data['description'],
                file=data['file']
            )

            return HttpResponse('Successfully created', status=201)
        else:
            return HttpResponse(f'Not correct field(s)\n{form.errors}', status=422)
    else:
        return HttpResponse('Method is not allowed', status=405)
