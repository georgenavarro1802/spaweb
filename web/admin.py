from django.contrib import admin
from web.models import (Suscripciones, Contacto, Persona, DatosEmpresa, Welcome, About, Testimonial, Popular, Gallery,
                        CategoriaServicio, Servicio, CategoriaProducto, Producto, Registros, ReservaProducto,
                        ReservaServicio, Team, Review, Newsletter, Unete, Especializacion)


class SuscripcionesAdmin(admin.ModelAdmin):
    list_display = ('email', 'fecha')
    ordering = ('fecha', )
    search_fields = ('email', )

admin.site.register(Suscripciones, SuscripcionesAdmin)


class PersonaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email')
    ordering = ('nombre', )
    search_fields = ('email', 'nombre')

admin.site.register(Persona, PersonaAdmin)


class ContactoAdmin(admin.ModelAdmin):
    list_display = ('persona', 'mensaje', 'fecha')
    ordering = ('fecha', 'persona')
    search_fields = ('persona__nombre', 'persona__email')

admin.site.register(Contacto, ContactoAdmin)


class DatosEmpresaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'celular', 'convencional',
                    'facebook', 'twitter', 'linkedin', 'instagram', 'googleplus',
                    'latitud', 'longitud', 'logoprincipal')
    ordering = ('nombre', )
    search_fields = ('nombre', 'email')

admin.site.register(DatosEmpresa, DatosEmpresaAdmin)


class WelcomeAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'descripcion', 'imagen1', 'tituloimagen1', 'imagen2', 'tituloimagen2', 'imagen3',
                    'tituloimagen3', 'imagen4', 'tituloimagen4')
    ordering = ('titulo', )
    search_fields = ('titulo', 'descripcion')

admin.site.register(Welcome, WelcomeAdmin)


class AboutAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'imagen1', 'tituloimagen1', 'imagen2', 'tituloimagen2')
    ordering = ('titulo', )
    search_fields = ('titulo', )

admin.site.register(About, AboutAdmin)


class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'testigo', 'testimonio', 'imagen_testigo')
    ordering = ('testigo', )
    search_fields = ('testigo', 'testimonio')

admin.site.register(Testimonial, TestimonialAdmin)


class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'descripcion', 'tituloimagen1', 'descripcionimagen1', 'imagen1',
                    'tituloimagen2', 'descripcionimagen2', 'imagen2')
    ordering = ('titulo', )
    search_fields = ('titulo', 'descripcion')

admin.site.register(Newsletter, NewsletterAdmin)


class UneteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'celular', 'especializacion', 'fecha', 'comentarios')
    ordering = ('fecha', 'nombre')
    search_fields = ('nombre', 'celular')
    list_filter = ('especializacion', )

admin.site.register(Unete, UneteAdmin)

admin.site.register(Especializacion)


class PopularAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'subtitulo1', 'subtitulo2', 'subtitulo3', 'imagen', 'tituloimagen')
    ordering = ('titulo', )
    search_fields = ('titulo', 'subtitulo1', 'subtitulo2', 'subtitulo3')

admin.site.register(Popular, PopularAdmin)


class GalleryAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'imagen1', 'tituloimagen1', 'imagen2', 'tituloimagen2', 'imagen3', 'tituloimagen3',
                    'imagen4', 'tituloimagen4', 'imagen5', 'tituloimagen5', 'imagen6', 'tituloimagen6',)
    ordering = ('tituloimagen1', )
    search_fields = ('tituloimagen1', 'tituloimagen2', 'tituloimagen3',
                     'tituloimagen4', 'tituloimagen5', 'tituloimagen6')

admin.site.register(Gallery, GalleryAdmin)


class TeamAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'imagen1', 'tituloimagen1', 'imagen2', 'tituloimagen2', 'imagen3', 'tituloimagen3',
                    'imagen4', 'tituloimagen4')
    ordering = ('tituloimagen1', )
    search_fields = ('tituloimagen1', 'tituloimagen2', 'tituloimagen3', 'tituloimagen4')

admin.site.register(Team, TeamAdmin)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('persona', 'review', 'foto', 'fecha')
    ordering = ('-fecha', )
    search_fields = ('persona', 'review')

admin.site.register(Review, ReviewAdmin)


admin.site.register(CategoriaServicio)
admin.site.register(CategoriaProducto)


class ServicioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'titulo', 'descripcion', 'categoria', 'duracion', 'precio', 'imagen')
    ordering = ('nombre', 'titulo', )
    search_fields = ('nombre', 'titulo', 'descripcion', 'categoria__nombre')
    list_filter = ('categoria', )

admin.site.register(Servicio, ServicioAdmin)


class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'titulo', 'descripcion', 'categoria', 'precio', 'imagen')
    ordering = ('nombre', 'titulo', )
    search_fields = ('nombre', 'titulo', 'descripcion', 'categoria__nombre')
    list_filter = ('categoria', )

admin.site.register(Producto, ProductoAdmin)


class RegistrosAdmin(admin.ModelAdmin):
    list_display = ('email', 'user', 'fecha', 'celular', 'convencional')
    ordering = ('fecha', 'email')
    search_fields = ('email', 'user__username')

admin.site.register(Registros, RegistrosAdmin)


class ReservaProductoAdmin(admin.ModelAdmin):
    list_display = ('registro', 'producto', 'fecha')
    ordering = ('fecha', )
    search_fields = ('producto__nombre', 'registro__user__username')

admin.site.register(ReservaProducto, ReservaProductoAdmin)


class ReservaServicioAdmin(admin.ModelAdmin):
    list_display = ('registro', 'servicio', 'fecha', 'fecha_servicio')
    ordering = ('fecha_servicio', )
    search_fields = ('servicio__nombre', 'registro__user__username')

admin.site.register(ReservaServicio, ReservaServicioAdmin)
