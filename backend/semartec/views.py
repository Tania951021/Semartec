from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
import logging
import requests
from .models import Contacto

logger = logging.getLogger(__name__)


def inicio(request):
    return render(request, 'index.html')


def enviar_correo_brevo(nombre, correo, mensaje):
    url = "https://api.brevo.com/v3/smtp/email"

    headers = {
        "accept": "application/json",
        "api-key": settings.BREVO_API_KEY,
        "content-type": "application/json"
    }

    data = {
        "sender": {
            "name": "Formulario Web",
            "email": settings.DEFAULT_FROM_EMAIL
        },
        "to": [
            {
                "email": settings.DEFAULT_FROM_EMAIL,
                "name": "Tania"
            }
        ],
        "subject": f"Nuevo mensaje de: {nombre}",
        "htmlContent": f"""
            <h3>Nuevo mensaje de contacto</h3>
            <p><b>Nombre:</b> {nombre}</p>
            <p><b>Correo:</b> {correo}</p>
            <p><b>Mensaje:</b><br>{mensaje}</p>
        """
    }

    # llamada HTTP rápida (sin SMTP, sin timeout)
    requests.post(url, json=data, headers=headers, timeout=10)


def contacto(request):
    if request.method == 'POST':
        try:
            nombre = request.POST.get('nombre', '').strip()
            correo = request.POST.get('correo', '').strip()
            mensaje = request.POST.get('mensaje', '').strip()

            if not nombre or not correo or not mensaje:
                return JsonResponse({'mensaje': '❌ Completa todos los campos'}, status=400)

            # Guarda en la base de datos
            Contacto.objects.create(
                nombre=nombre,
                correo=correo,
                mensaje=mensaje
            )

            # Envía el correo por Brevo API
            enviar_correo_brevo(nombre, correo, mensaje)

            return JsonResponse({'mensaje': 'Mensaje enviado correctamente'})

        except Exception as e:
            error_texto = f"Error: {type(e).__name__} - {str(e)}"
            logger.error(error_texto)
            return JsonResponse({'mensaje': error_texto}, status=500)

    return JsonResponse({'mensaje': 'Método no permitido'}, status=405)