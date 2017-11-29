import json
import random
from datetime import datetime, timedelta

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from spaweb.settings import (NOMBRE_INSTITUCION, SEGUNDOS_CIERRE_SESION, SUSCRIPCION_EMAILS, CONTACTO_EMAILS,
                             RESERVA_ESTADO_CONFIRMADO, RESERVA_ESTADO_PENDIENTE)
from web.models import (Suscripciones, Contacto, Persona, DatosEmpresa, Welcome, About, Testimonial, Popular, Gallery,
                        CategoriaServicio, Servicio, Producto, CategoriaProducto, Registros, ReservaProducto,
                        ReservaServicio, Team, Review, Newsletter, Unete, Especializacion)
from web.tareas import send_html_mail


def convertir_fecha(s):
    """
    :param s: dd-mm-YYYY
    :return: datetime YYYY-mm-dd
    """
    try:
        return datetime(int(s[-4:]), int(s[3:5]), int(s[:2])).date()
    except:
        return datetime.today()


def construccion(request):
    datos = {'datosempresa': DatosEmpresa.objects.all()[0]}
    return render(request, "construccion.html", datos)


def entrar(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        user = request.POST['user']
        clave = request.POST['pass']
        if User.objects.filter(username=user).exists():
            u = User.objects.filter(username=user)[0]
            usuario = authenticate(username=u.username, password=clave)
            if usuario:
                login(request, usuario)
                if 'next' in request.POST:
                    return HttpResponse(json.dumps({'result': 'ok'}), content_type="application/json")
                return HttpResponse(json.dumps({'result': 'ok'}), content_type="application/json")
            else:
                return HttpResponse(json.dumps({'result': 'error_password'}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({'result': 'error_email'}), content_type="application/json")
    else:
        datos = {}
        if 'next' in request.GET:
            datos['next'] = request.GET['next']
        return render(request, "register.html", datos)


def salir(request):
    logout(request)
    if 'next' in request.GET:
        return HttpResponseRedirect("/?next=%s" % (request.GET['next']))
    return HttpResponseRedirect("/")


def home(request):
    if 'ultimo_acceso' not in request.session:
        request.session['ultimo_acceso'] = str(datetime.now())
    
    registro = None
    if request.user and not request.user.is_anonymous():
        if Registros.objects.filter(user=request.user).exists():
            registro = Registros.objects.filter(user=request.user)[0]

    popular = Popular.objects.all()[0]
    popular_descripcion1 = popular.descripcion1.split(":")
    popular_descripcion2 = popular.descripcion2.split(":")
    popular_descripcion3 = popular.descripcion3.split(":")
    popular_descripcionimagen = popular.descripcionimagen.split(":")

    about_list = About.objects.all()[:2]
    about_titulo = about_list[0].titulo
    return render(request, "index.html",
                  {
                      'title': NOMBRE_INSTITUCION + ' | Web Page',
                      'datosempresa': DatosEmpresa.objects.all()[0],
                      'welcome': Welcome.objects.all()[0],
                      'about_titulo': about_titulo,
                      'about_list': about_list,
                      'testimonial': Testimonial.objects.all()[0],
                      'newsletter': Newsletter.objects.all()[0],
                      'popular': popular,
                      'gallery': Gallery.objects.all()[0],
                      'team': Team.objects.all()[0],
                      'reviews': Review.objects.all()[:4],
                      'registro': registro,
                      'popular_descripcion1': popular_descripcion1,
                      'popular_descripcion2': popular_descripcion2,
                      'popular_descripcion3': popular_descripcion3,
                      'popular_descripcionimagen': popular_descripcionimagen,
                      'especializaciones': Especializacion.objects.all(),
                      'cantidad_reservas': registro.cantidad_total_reservas() if registro else 0
                  })


def servicios(request):
    if 'ultimo_acceso' not in request.session:
        request.session['ultimo_acceso'] = str(datetime.now())

    registro = None
    if request.user and not request.user.is_anonymous() and Registros.objects.filter(user=request.user).exists():
        registro = Registros.objects.filter(user=request.user)[0]

    datos = {
        'title': NOMBRE_INSTITUCION + ' | Services',
        'datosempresa': DatosEmpresa.objects.all()[0],
        'categorias_servicios': CategoriaServicio.objects.all(),
        'servicios': Servicio.objects.all(),
        'registro': registro,
        'unmes': datetime.today() + timedelta(days=30),
        'cantidad_reservas': registro.cantidad_total_reservas() if registro else 0
    }
    return render(request, "services.html", datos)


def productos(request):
    if 'ultimo_acceso' not in request.session:
        request.session['ultimo_acceso'] = str(datetime.now())

    registro = None
    if request.user and not request.user.is_anonymous() and Registros.objects.filter(user=request.user).exists():
        registro = Registros.objects.filter(user=request.user)[0]

    datos = {
        'title': NOMBRE_INSTITUCION + ' | Products',
        'datosempresa': DatosEmpresa.objects.all()[0],
        'categorias_productos': CategoriaProducto.objects.all(),
        'productos': Producto.objects.all(),
        'registro': registro,
        'cantidad_reservas': registro.cantidad_total_reservas() if registro else 0
    }
    return render(request, "products.html", datos)


@login_required(login_url='/')
def reservas(request):
    if 'ultimo_acceso' not in request.session:
        request.session['ultimo_acceso'] = str(datetime.now())

    if request.method == 'POST':
        if 'action' in request.POST:
            action = request.POST['action']
            if action == 'reserva_productos':
                try:
                    registro = Registros.objects.get(pk=request.POST['rid'])
                    producto = Producto.objects.get(pk=request.POST['pid'])
                    if not ReservaProducto.objects.filter(registro=registro, producto=producto).exists():
                        reserva_producto = ReservaProducto(registro=registro,
                                                           producto=producto,
                                                           fecha=datetime.today())
                        reserva_producto.save()
                        return HttpResponse(json.dumps({'result': 'ok'}), content_type="application/json")
                    else:
                        return HttpResponse(json.dumps({'result': 'exist',
                                                        'mensaje': 'Ya existe una reserva del producto en su '
                                                                   'listado de reservas'}),
                                            content_type="application/json")
                except Exception:
                    return HttpResponse(json.dumps({'result': 'bad',
                                                    'mensaje': 'Ocurrió un error al guardar los datos. '
                                                               'Inténtelo mas tarde'}),
                                        content_type="application/json")

            if action == 'reserva_servicios':
                registro = Registros.objects.get(pk=request.POST['rid'])
                servicio = Servicio.objects.get(pk=request.POST['sid'])

                fechaservicio = datetime.today()
                if 'fechaserv' in request.POST and request.POST['fechaserv'] != '':
                    fechaservicio = convertir_fecha(request.POST['fechaserv'])
                if not ReservaServicio.objects.filter(registro=registro, 
                                                      servicio=servicio, 
                                                      estado=RESERVA_ESTADO_PENDIENTE).exists():
                    reserva_servicio = ReservaServicio(registro=registro,
                                                       servicio=servicio,
                                                       fecha=datetime.today(),
                                                       fecha_servicio=fechaservicio)
                    reserva_servicio.save()
                    return HttpResponse(json.dumps({'result': 'ok'}), content_type="application/json")
                else:
                    return HttpResponse(json.dumps({'result': 'exist',
                                                    'mensaje': 'Ya existe una reserva pendiente del servicio '
                                                               'en su lista de reservas'}),
                                        content_type="application/json")

            if action == 'confirmar_reserva_producto':
                reserva = ReservaProducto.objects.get(pk=request.POST['rid'])
                cantidad = int(request.POST['cant'])
                reserva.estado = RESERVA_ESTADO_CONFIRMADO
                reserva.cantidad = cantidad
                reserva.save()
                send_html_mail("Reserva de Producto en ENLIVEN WEB", 
                               "emails/reserva_prod.html", 
                               {'reserva': reserva}, 
                               CONTACTO_EMAILS)
                return HttpResponse(json.dumps({'result': 'ok'}), content_type="application/json")

            if action == 'confirmar_reserva_servicio':
                reserva = ReservaServicio.objects.get(pk=request.POST['rid'])
                reserva.estado = RESERVA_ESTADO_CONFIRMADO
                reserva.save()
                send_html_mail("Reserva de Servicio en ENLIVEN WEB",
                               "emails/reserva_serv.html", 
                               {'reserva': reserva}, 
                               CONTACTO_EMAILS)
                return HttpResponse(json.dumps({'result': 'ok'}), content_type="application/json")

        return HttpResponse(json.dumps({'result': 'bad', 'mensaje': 'Solicitud Incorrecta'}),
                            content_type="application/json")
    else:
        if 'action' in request.GET:
            action = request.GET['action']

            if action == 'eliminar_reserva_producto':
                reserva = ReservaProducto.objects.get(pk=request.GET['id'])
                reserva.delete()

            if action == 'eliminar_reserva_servicio':
                reserva = ReservaServicio.objects.get(pk=request.GET['id'])
                reserva.delete()

            return HttpResponseRedirect("/reservas")
        else:
            try:
                datos = {'title': NOMBRE_INSTITUCION + ' | Reservas'}
                datos['registro'] = registro = Registros.objects.get(user=request.user)
                datos['datosempresa'] = DatosEmpresa.objects.all()[0]
                datos['reserva_productos'] = registro.mis_reservas_productos()
                datos['reserva_servicios'] = registro.mis_reservas_servicios()
                datos['cantidad_reservas'] = registro.cantidad_total_reservas() if registro else 0
                return render(request, "reservas.html", datos)
            except Exception:
                return HttpResponseRedirect("/")


def register(request):
    if 'ultimo_acceso' not in request.session:
        request.session['ultimo_acceso'] = str(datetime.now())

    if request.method == 'POST':
        try:
            with transaction.atomic():
                email = request.POST['email']
                clave = request.POST['pass']
                celular = request.POST['celular']
                convencional = request.POST['convencional']
                if User.objects.filter(username=email).exists():
                    u = User.objects.filter(username=email)[0]
                else:
                    u = User(username=email, email=email)
                u.set_password(clave)
                u.save()
                registro = Registros(fecha=datetime.today(),
                                     email=email,
                                     user=u,
                                     celular=celular,
                                     convencional=convencional)
                registro.save()
                send_html_mail("Registro exitoso en ENLIVEN WEB", "emails/registro.html", {'email': email}, [email])
                return HttpResponse(json.dumps({'result': 'ok', 'user': registro.user.username}),
                                    content_type="application/json")
        except Exception:
            return HttpResponse(json.dumps({'result': 'bad'}), content_type="application/json")
    else:
        datos = {
            'title': NOMBRE_INSTITUCION + ' | Register', 
            'datosempresa': DatosEmpresa.objects.all()[0]
        }
        return render(request, "register.html", datos)


def lost_password(request):
    if 'ultimo_acceso' not in request.session:
        request.session['ultimo_acceso'] = str(datetime.now())

    if request.method == 'POST':
        try:
            with transaction.atomic():
                email = request.POST['email']
                if User.objects.filter(username=email).exists():
                    u = User.objects.filter(username=email)[0]
                    nueva_clave = ""
                    for a in range(4):
                        nueva_clave += str(random.randint(1, 10))
                    u.set_password(nueva_clave)
                    u.save()
                    datos = {'email': email, 'password': nueva_clave}
                    send_html_mail("Generated Password from ENLIVEN WEB", "emails/lost_password.html", datos, [email])
                    return HttpResponse(json.dumps({'result': 'ok'}), content_type="application/json")
                else:
                    return HttpResponse(json.dumps({'result': 'error_email'}), content_type="application/json")
        
        except Exception:
            return HttpResponse(json.dumps({'result': 'bad'}), content_type="application/json")
    else:
        datos = {
            'title': NOMBRE_INSTITUCION + ' | Recovery Password',
            'datosempresa': DatosEmpresa.objects.all()[0]
        }
        return render(request, "lost_password.html", datos)


def checksession(request):
    try:
        if 'ultimo_acceso' in request.session:
            fa = request.session['ultimo_acceso']
        else:
            request.session['ultimo_acceso'] = fa = datetime.now()
        
        nuevasesion = False
        if SEGUNDOS_CIERRE_SESION:
            if (fa + timedelta(seconds=SEGUNDOS_CIERRE_SESION)) < datetime.now():
                nuevasesion = True
        return HttpResponse(json.dumps({'result': 'ok', 'nuevasesion': nuevasesion}), content_type="application/json")
    
    except Exception:
        return HttpResponse(json.dumps({"result": "bad"}), content_type="application/json")


def suscripciones(request):
    try:
        if not Suscripciones.objects.filter(email=request.POST['email']).exists():
            suscripcion = Suscripciones(email=request.POST['email'])
            suscripcion.save()
            datos = {'email': suscripcion.email, 'cantidad': Suscripciones.objects.all().count()}
            send_html_mail("Suscripción ENLIVEN WEB Home", 
                           "emails/suscripcion_login.html", 
                           datos, 
                           SUSCRIPCION_EMAILS)
            send_html_mail("Gracias por suscribirte - ENLIVEN WEB", 
                           "emails/suscripcion_senduser.html", 
                           datos, 
                           [suscripcion.email])
        return HttpResponse(json.dumps({"result": "ok"}), content_type="application/json")
    
    except Exception:
        return HttpResponse(json.dumps({"result": "bad"}), content_type="application/json")


def unete(request):
    try:
        if not Unete.objects.filter(nombre=request.POST['nombre'], celular=request.POST['celular']).exists():
            unete = Unete(nombre=request.POST['nombre'],
                          celular=request.POST['celular'],
                          especializacion=Especializacion.objects.get(pk=int(request.POST['especializacion'])),
                          comentarios=request.POST['comentarios'])
            unete.save()
            send_html_mail("Se ha unido a SPA ENLIVEN WEB", "emails/unete.html", {'unete': unete}, CONTACTO_EMAILS)
        return HttpResponse(json.dumps({"result": "ok"}), content_type="application/json")
    
    except Exception:
        return HttpResponse(json.dumps({"result": "bad"}), content_type="application/json")


def contactos(request):
    try:
        nombre = request.POST['nombre']
        email = request.POST['email']
        mensaje = request.POST['mensaje']
        if not Persona.objects.filter(nombre=nombre, email=email).exists():
            persona = Persona(nombre=nombre, email=email)
            persona.save()
        else:
            persona = Persona.objects.filter(nombre=nombre, email=email)[0]

        contacto = Contacto(persona=persona, mensaje=mensaje)
        contacto.save()
        datos = {
            'nombre': contacto.persona.nombre,
            'email': contacto.persona.email,
            'mensaje': contacto.mensaje
        }
        send_html_mail("Mensaje Recibido ENLIVEN WEB Contact Form", 
                       "emails/usermensaje.html", 
                       datos, 
                       CONTACTO_EMAILS)
        return HttpResponse(json.dumps({"result": "ok"}), content_type="application/json")
    
    except Exception:
        return HttpResponse(json.dumps({"result": "bad"}), content_type="application/json")
