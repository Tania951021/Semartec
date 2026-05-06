from django.shortcuts import render
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from .models import Contacto


def inicio(request):
    return render(request, 'index.html')


def contacto(request):
    if request.method == 'POST':
        try:
            nombre = request.POST.get('nombre')
            correo = request.POST.get('correo')
            mensaje = request.POST.get('mensaje')

            Contacto.objects.create(
                nombre=nombre,
                correo=correo,
                mensaje=mensaje
            )

            send_mail(
                subject='Nuevo mensaje',
                message=mensaje,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.EMAIL_HOST_USER],
            )

            return JsonResponse({'mensaje': 'Mensaje enviado correctamente'})

        except Exception as e:
            print("ERROR REAL:", e)
            return JsonResponse({'mensaje': str(e)}, status=500)

    return JsonResponse({'mensaje': 'Método no permitido'}, status=405)