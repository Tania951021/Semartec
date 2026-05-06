from django.shortcuts import render
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
import logging 
from .models import Contacto

logger = logging.getLogger(__name__)

def inicio(request):
    return render(request, 'index.html')


def contacto(request):
    if request.method == 'POST':
        try:
            nombre = request.POST.get('nombre', '').strip()
            correo = request.POST.get('correo', '').strip()
            mensaje = request.POST.get('mensaje', '').strip()

            if not nombre or not correo or not mensaje:
                return JsonResponse({'mensaje': '❌ Completa todos los campos'}, status=400)

            Contacto.objects.create(
                nombre=nombre,
                correo=correo,
                mensaje=mensaje
            )

            asunto = f'Nuevo mensaje de: {nombre}'
            cuerpo = f"""
            Nombre: {nombre}
            Correo: {correo}
            
            Mensaje:
            {mensaje}
            """

            send_mail(
                subject=asunto,
                message=cuerpo,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=False,
            )

            return JsonResponse({'mensaje': 'Mensaje enviado correctamente'})

        except Exception as e:
            error_texto = f"Error: {type(e).__name__} - {str(e)}"
            logger.error(error_texto)
            print(error_texto)  
            return JsonResponse({'mensaje': error_texto}, status=500)

    return JsonResponse({'mensaje': 'Método no permitido'}, status=405)