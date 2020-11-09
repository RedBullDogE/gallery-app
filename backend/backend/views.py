from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt

from .forms import RegisterForm


@csrf_exempt  # TODO
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')

            user, created = get_user_model().objects.get_or_create(
                username=username,
                defaults={'email': email,
                          'password': password}
            )

            if not created:
                return HttpResponse('User already exists', status=409)

            return HttpResponse('Registered', status=201)

        return HttpResponse(f'Not correct field(s)\n{form.errors}', status=422)
