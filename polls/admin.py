from django.contrib import admin
from .models import User,Producto,Carro,Busqueda
# Register your models here.
admin.site.register(User)
admin.site.register(Producto)
admin.site.register(Carro)
admin.site.register(Busqueda)