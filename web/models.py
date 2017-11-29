from django.contrib.auth.models import User
from django.db import models

from spaweb.settings import (RESERVA_ESTADO_PENDIENTE, RESERVA_ESTADO_CONFIRMADO,
                             RESERVA_ESTADO_RECIBIDO, RESERVA_ESTADO_RECHAZADO)


class Especializacion(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return "{}".format(self.nombre)

    class Meta:
        verbose_name = "Especializacion"
        verbose_name_plural = "Especializaciones"
        ordering = ('nombre', )
        db_table = 'especializaciones'

    def save(self, force_insert=False, force_update=False, using=None, **kwargs):
        self.nombre = self.nombre.upper()
        super(Especializacion, self).save(force_insert, force_update, using)


class Suscripciones(models.Model):
    email = models.CharField(max_length=300)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} ({})".format(self.email, self.fecha.strftime('%d-%m-%Y'))

    class Meta:
        verbose_name = "Suscripcion"
        verbose_name_plural = "Suscripciones"
        db_table = 'suscripciones'


class Unete(models.Model):
    nombre = models.CharField(max_length=300)
    celular = models.CharField(max_length=20)
    especializacion = models.ForeignKey(Especializacion, blank=True, null=True)
    comentarios = models.TextField(blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} - {} ({})".format(self.nombre, self.celular, self.fecha.strftime('%d-%m-%Y'))

    class Meta:
        verbose_name = "Unete a nosotros"
        verbose_name_plural = "Unete a nosotros"
        db_table = 'uniones'

    def save(self, force_insert=False, force_update=False, using=None, **kwargs):
        self.nombre = self.nombre.upper()
        self.comentarios = self.comentarios.upper()
        super(Unete, self).save(force_insert, force_update, using)


class Persona(models.Model):
    nombre = models.CharField(max_length=300)
    email = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return "{} ({})".format(self.nombre, self.email)

    class Meta:
        verbose_name = "Persona"
        verbose_name_plural = "Personas"
        db_table = 'personas'


class Contacto(models.Model):
    persona = models.ForeignKey(Persona)
    mensaje = models.TextField(blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} ({})".format(self.persona, self.fecha.strftime('%d-%m-%Y'))

    class Meta:
        verbose_name = "Contacto"
        verbose_name_plural = "Contactos"
        db_table = 'contactos'


# Datos para parametrizacion de elementos y contenidos
class DatosEmpresa(models.Model):
    nombre = models.CharField(max_length=300)
    email = models.CharField(max_length=200, blank=True, null=True)
    celular = models.CharField(max_length=50, blank=True, null=True)
    convencional = models.CharField(max_length=50, blank=True, null=True)
    facebook = models.CharField(max_length=200, blank=True, null=True)
    twitter = models.CharField(max_length=200, blank=True, null=True)
    linkedin = models.CharField(max_length=200, blank=True, null=True)
    googleplus = models.CharField(max_length=200, blank=True, null=True)
    instagram = models.CharField(max_length=200, blank=True, null=True)
    latitud = models.CharField(max_length=50, verbose_name=u'Latitud', blank=True, null=True)
    longitud = models.CharField(max_length=50, verbose_name=u'Longitud', blank=True, null=True)
    logoprincipal = models.FileField(upload_to='logos/%Y/%m/%d', max_length=200, blank=True, null=True)
    descripcion1 = models.TextField(blank=True, null=True)
    descripcion2 = models.TextField(blank=True, null=True)
    slogan = models.CharField(max_length=150, blank=True, null=True)
    seccion_team = models.BooleanField(default=False)
    seccion_testimonial = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Datos Generales"
        verbose_name_plural = "Datos Generales"
        db_table = 'empresa'

    def download_logo(self):
        return self.logoprincipal.url

    def save(self, force_insert=False, force_update=False, using=None, **kwargs):
        if self.nombre:
            self.nombre = self.nombre.upper()
        if self.email:
            self.email = self.email.lower()
        if self.facebook:
            self.facebook = self.facebook.lower()
        if self.twitter:
            self.twitter = self.twitter.lower()
        if self.linkedin:
            self.linkedin = self.linkedin.lower()
        super(DatosEmpresa, self).save(force_insert, force_update, using)


# Welcome
class Welcome(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    imagen1 = models.FileField(upload_to='welcome/%Y/%m/%d', max_length=200)
    tituloimagen1 = models.CharField(max_length=100, blank=True, null=True)
    descripcionimagen1 = models.CharField(max_length=150, blank=True, null=True)

    imagen2 = models.FileField(upload_to='welcome/%Y/%m/%d', max_length=200)
    tituloimagen2 = models.CharField(max_length=100, blank=True, null=True)
    descripcionimagen2 = models.CharField(max_length=150, blank=True, null=True)

    imagen3 = models.FileField(upload_to='welcome/%Y/%m/%d', max_length=200)
    tituloimagen3 = models.CharField(max_length=100, blank=True, null=True)
    descripcionimagen3 = models.CharField(max_length=150, blank=True, null=True)

    imagen4 = models.FileField(upload_to='welcome/%Y/%m/%d', max_length=200)
    tituloimagen4 = models.CharField(max_length=100, blank=True, null=True)
    descripcionimagen4 = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = "Seccion Welcome"
        verbose_name_plural = "Seccion Welcome"
        db_table = 'seccion_welcome'

    def download_imagen1(self):
        return self.imagen1.url

    def download_imagen2(self):
        return self.imagen2.url

    def download_imagen3(self):
        return self.imagen3.url

    def download_imagen4(self):
        return self.imagen4.url


# About
class About(models.Model):
    titulo = models.CharField(max_length=100)

    imagen1 = models.FileField(upload_to='about/%Y/%m/%d', max_length=200)
    tituloimagen1 = models.CharField(max_length=100, blank=True, null=True)
    descripcionimagen1 = models.CharField(max_length=300, blank=True, null=True)

    imagen2 = models.FileField(upload_to='about/%Y/%m/%d', max_length=200)
    tituloimagen2 = models.CharField(max_length=100, blank=True, null=True)
    descripcionimagen2 = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = "Seccion Experiencia"
        verbose_name_plural = "Seccion Experiencia"
        db_table = 'seccion_about'

    def download_imagen1(self):
        return self.imagen1.url

    def download_imagen2(self):
        return self.imagen2.url


# Testimonials
class Testimonial(models.Model):
    titulo = models.CharField(max_length=100, blank=True, null=True)

    testigo = models.CharField(max_length=100)
    testimonio = models.TextField(blank=True, null=True)
    imagen_testigo = models.FileField(upload_to='testimonials/%Y/%m/%d', max_length=200)

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = "Seccion Testimonial"
        verbose_name_plural = "Seccion Testimonial"
        db_table = 'seccion_testimonial'

    def download_imagen_testigo(self):
        return self.imagen_testigo.url


# Newsletter
class Newsletter(models.Model):
    titulo = models.CharField(max_length=100, blank=True, null=True)
    descripcion = models.CharField(max_length=300, blank=True, null=True)

    tituloimagen1 = models.CharField(max_length=100, blank=True, null=True)
    descripcionimagen1 = models.CharField(max_length=200, blank=True, null=True)
    imagen1 = models.FileField(upload_to='Newsletter/%Y/%m/%d', max_length=200, blank=True, null=True)

    tituloimagen2 = models.CharField(max_length=100, blank=True, null=True)
    descripcionimagen2 = models.CharField(max_length=200, blank=True, null=True)
    imagen2 = models.FileField(upload_to='Newsletter/%Y/%m/%d', max_length=200, blank=True, null=True)

    def __str__(self):
        return "{} - {}".format(self.titulo, self.descripcion)

    class Meta:
        verbose_name = "Seccion Newsletter"
        verbose_name_plural = "Seccion Newsletter"
        db_table = 'seccion_newsletter'

    def download_imagen1(self):
        return self.imagen1.url

    def download_imagen2(self):
        return self.imagen2.url


# Popular
class Popular(models.Model):
    titulo = models.CharField(max_length=100)

    subtitulo1 = models.CharField(max_length=100, blank=True, null=True)
    descripcion1 = models.CharField(max_length=200, blank=True, null=True)
    imagen1 = models.FileField(upload_to='popular/%Y/%m/%d', max_length=200, blank=True, null=True)
    subtitulo2 = models.CharField(max_length=100, blank=True, null=True)
    descripcion2 = models.CharField(max_length=200, blank=True, null=True)
    imagen2 = models.FileField(upload_to='popular/%Y/%m/%d', max_length=200, blank=True, null=True)
    subtitulo3 = models.CharField(max_length=100, blank=True, null=True)
    descripcion3 = models.CharField(max_length=200, blank=True, null=True)
    imagen3 = models.FileField(upload_to='popular/%Y/%m/%d', max_length=200, blank=True, null=True)

    imagen = models.FileField(upload_to='popular/%Y/%m/%d', max_length=200, blank=True, null=True)
    tituloimagen = models.CharField(max_length=100, blank=True, null=True)
    descripcionimagen = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = "Seccion Popular"
        verbose_name_plural = "Seccion Popular"
        db_table = 'seccion_popular'

    def download_imagen(self):
        return self.imagen.url

    def download_imagen1(self):
        return self.imagen1.url

    def download_imagen2(self):
        return self.imagen2.url

    def download_imagen3(self):
        return self.imagen3.url


# Gallery
class Gallery(models.Model):
    titulo = models.CharField(max_length=100, blank=True, null=True)

    imagen1 = models.FileField(upload_to='gallery/%Y/%m/%d', max_length=200, blank=True, null=True)
    tituloimagen1 = models.CharField(max_length=100, blank=True, null=True)
    descripcionimagen1 = models.CharField(max_length=300, blank=True, null=True)

    imagen2 = models.FileField(upload_to='gallery/%Y/%m/%d', max_length=200, blank=True, null=True)
    tituloimagen2 = models.CharField(max_length=100, blank=True, null=True)
    descripcionimagen2 = models.CharField(max_length=300, blank=True, null=True)

    imagen3 = models.FileField(upload_to='gallery/%Y/%m/%d', max_length=200, blank=True, null=True)
    tituloimagen3 = models.CharField(max_length=100, blank=True, null=True)
    descripcionimagen3 = models.CharField(max_length=300, blank=True, null=True)

    imagen4 = models.FileField(upload_to='gallery/%Y/%m/%d', max_length=200, blank=True, null=True)
    tituloimagen4 = models.CharField(max_length=100, blank=True, null=True)
    descripcionimagen4 = models.CharField(max_length=300, blank=True, null=True)

    imagen5 = models.FileField(upload_to='gallery/%Y/%m/%d', max_length=200, blank=True, null=True)
    tituloimagen5 = models.CharField(max_length=100, blank=True, null=True)
    descripcionimagen5 = models.CharField(max_length=300, blank=True, null=True)

    imagen6 = models.FileField(upload_to='gallery/%Y/%m/%d', max_length=200, blank=True, null=True)
    tituloimagen6 = models.CharField(max_length=100, blank=True, null=True)
    descripcionimagen6 = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return "Gallery"

    class Meta:
        verbose_name = "Seccion Gallery"
        verbose_name_plural = "Seccion Gallery"
        db_table = 'seccion_gallery'

    def download_imagen1(self):
        return self.imagen1.url

    def download_imagen2(self):
        return self.imagen2.url

    def download_imagen3(self):
        return self.imagen3.url

    def download_imagen4(self):
        return self.imagen4.url

    def download_imagen5(self):
        return self.imagen5.url

    def download_imagen6(self):
        return self.imagen6.url


# Team
class Team(models.Model):
    titulo = models.CharField(max_length=100, blank=True, null=True)

    imagen1 = models.FileField(upload_to='team/%Y/%m/%d', max_length=200, blank=True, null=True)
    tituloimagen1 = models.CharField(max_length=100, blank=True, null=True)
    descripcionimagen1 = models.CharField(max_length=300, blank=True, null=True)

    imagen2 = models.FileField(upload_to='team/%Y/%m/%d', max_length=200, blank=True, null=True)
    tituloimagen2 = models.CharField(max_length=100, blank=True, null=True)
    descripcionimagen2 = models.CharField(max_length=300, blank=True, null=True)

    imagen3 = models.FileField(upload_to='team/%Y/%m/%d', max_length=200, blank=True, null=True)
    tituloimagen3 = models.CharField(max_length=100, blank=True, null=True)
    descripcionimagen3 = models.CharField(max_length=300, blank=True, null=True)

    imagen4 = models.FileField(upload_to='team/%Y/%m/%d', max_length=200, blank=True, null=True)
    tituloimagen4 = models.CharField(max_length=100, blank=True, null=True)
    descripcionimagen4 = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return "Team"

    class Meta:
        verbose_name = "Seccion Team"
        verbose_name_plural = "Seccion Team"
        db_table = 'seccion_team'

    def download_imagen1(self):
        return self.imagen1.url

    def download_imagen2(self):
        return self.imagen2.url

    def download_imagen3(self):
        return self.imagen3.url

    def download_imagen4(self):
        return self.imagen4.url


# Reviews
class Review(models.Model):
    persona = models.CharField(max_length=100)
    review = models.CharField(max_length=300, blank=True, null=True)
    foto = models.FileField(upload_to='reviews/%Y/%m/%d', max_length=200, blank=True, null=True)
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return "Reviews"

    class Meta:
        verbose_name = "Seccion Review"
        verbose_name_plural = "Seccion Reviews"
        db_table = 'seccion_review'
        ordering = ('-fecha', )

    def download_foto(self):
        return self.foto.url


# Models para la APP
class CategoriaServicio(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Categoria - Servicio "
        verbose_name_plural = "Categorias - Servicios"
        db_table = 'categorias_servicios'
        ordering = ('nombre', )


class CategoriaProducto(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Categoria - Producto "
        verbose_name_plural = "Categorias - Productos"
        db_table = 'categorias_productos'
        ordering = ('nombre', )


class Servicio(models.Model):
    nombre = models.CharField(max_length=50)
    titulo = models.CharField(max_length=50, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    categoria = models.ForeignKey(CategoriaServicio, blank=True, null=True)
    duracion = models.IntegerField(default=0)
    precio = models.FloatField(default=0)
    imagen = models.FileField(upload_to='servicios', max_length=200, blank=True, null=True)

    def __str__(self):
        return "{} ({})".format(self.titulo, self.categoria.nombre)

    class Meta:
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"
        db_table = 'servicios'

    def download_imagen(self):
        return self.imagen.url

    def nombre_compuesto(self):
        return "{} - {}".format(self.nombre, self.titulo)


class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    titulo = models.CharField(max_length=50, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    categoria = models.ForeignKey(CategoriaProducto, blank=True, null=True)
    precio = models.FloatField(default=0)
    imagen = models.FileField(upload_to='productos', max_length=200, blank=True, null=True)

    def __str__(self):
        return "{} ({})".format(self.titulo, self.categoria.nombre)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        db_table = 'productos'

    def download_imagen(self):
        return self.imagen.url

    def nombre_compuesto(self):
        return "{} - {}".format(self.nombre, self.titulo)


class Registros(models.Model):
    email = models.CharField(max_length=300)
    user = models.ForeignKey(User, blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    celular = models.CharField(max_length=100, blank=True, null=True)
    convencional = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return "{} ({})".format(self.email, self.user.username)

    class Meta:
        verbose_name = "Registros"
        verbose_name_plural = "Registros"
        db_table = 'registros'
        unique_together = ('user', )

    def mis_reservas_productos(self):
        return self.reservaproducto_set.all()

    def cantidad_reservas_productos(self):
        return self.reservaproducto_set.count()

    def mis_reservas_servicios(self):
        return self.reservaservicio_set.all()

    def cantidad_reservas_servicios(self):
        return self.reservaservicio_set.count()

    def cantidad_total_reservas(self):
        return self.cantidad_reservas_productos() + self.cantidad_reservas_servicios()

ESTADOS = (
    (RESERVA_ESTADO_PENDIENTE, 'Pendiente'),
    (RESERVA_ESTADO_CONFIRMADO, 'Confirmado'),
    (RESERVA_ESTADO_RECIBIDO, 'Recibido'),
    (RESERVA_ESTADO_RECHAZADO, 'Rechazado')
)


class ReservaProducto(models.Model):
    registro = models.ForeignKey(Registros)
    producto = models.ForeignKey(Producto)
    cantidad = models.IntegerField(default=1)
    estado = models.IntegerField(default=RESERVA_ESTADO_PENDIENTE, choices=ESTADOS)
    fecha = models.DateField(blank=True, null=True)

    def __str__(self):
        return "Reserva Producto {} ({})".format(self.producto.nombre, self.registro.user.username)

    class Meta:
        verbose_name = "Reserva Producto"
        verbose_name_plural = "Reservas Productos"
        db_table = 'reservas_productos'
        ordering = ('fecha', )


class ReservaServicio(models.Model):
    registro = models.ForeignKey(Registros)
    servicio = models.ForeignKey(Servicio)
    estado = models.IntegerField(default=RESERVA_ESTADO_PENDIENTE, choices=ESTADOS)
    fecha = models.DateField(blank=True, null=True)
    fecha_servicio = models.DateField(blank=True, null=True)

    def __str__(self):
        return "Reserva Servicio {} ({})".format(self.servicio.nombre, self.registro.user.username)

    class Meta:
        verbose_name = "Reserva Servicio"
        verbose_name_plural = "Reservas Servicios"
        db_table = 'reservas_servicios'
        ordering = ('fecha', )
