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
            nombre = request.POST.get('nombre', '').strip()
            correo = request.POST.get('correo', '').strip()
            mensaje = request.POST.get('mensaje', '').strip()

            if not nombre or not correo or not mensaje:
                return JsonResponse(
                    {'mensaje': 'Por favor completa todos los campos.'}, 
                    status=400
                )

            Contacto.objects.create(
                nombre=nombre,
                correo=correo,
                mensaje=mensaje
            )

            asunto = f'Nuevo mensaje de contacto: {nombre}'
            cuerpo = f"""
            Has recibido un nuevo mensaje desde el formulario de la web:

            Nombre: {nombre}
            Correo: {correo}
            Mensaje:
            {mensaje}
            """

            # Enviar correo con configuración segura
            send_mail(
                subject=asunto,
                message=cuerpo,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=False,  
            )

            return JsonResponse({'mensaje': '✅ Mensaje enviado correctamente'})

        except Exception as e:
            print("ERROR REAL:", e) 
            return JsonResponse({'mensaje': f'Error: {str(e)}'}, status=500)

    return JsonResponse({'mensaje': ' Método no permitido'}, status=405)