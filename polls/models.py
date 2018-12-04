from django.db import models
from datetime import datetime, timedelta   
from django.contrib.auth.models import User 
from .managers import UserManager
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
	username = models.CharField(primary_key=True, max_length=50, unique=True)
	email = models.EmailField(unique=True)
	fecha_nacimiento = models.CharField(max_length=50)
	is_staff = models.BooleanField(default=False)	
	is_active = models.BooleanField(default=False)

	objects = UserManager()

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ["email"]

	class Meta:
		verbose_name = u'Usuario'
		verbose_name_plural = u'Usuarios'

class Producto(models.Model):
	Codigo_barras= models.IntegerField(primary_key=True, unique=True)
	Nombre=models.CharField(max_length=50)
	Tienda=models.CharField(max_length=50)
	Precio=models.IntegerField()
	Descripcion=models.CharField(max_length=1000)

	class Meta:
		verbose_name= u'Producto'
		verbose_name_plural = u'Producto'


class Carro(models.Model):
	idCarro=models.AutoField(primary_key=True, unique=True)
	CodigoFactura=models.CharField(max_length=50)
	Codigo_barras=models.ForeignKey(Producto,on_delete=models.CASCADE)
	username=models.ForeignKey(User, on_delete=models.CASCADE)
	Cantidad=models.IntegerField()
	Vendido=models.BooleanField(default=False)

	class Meta:
		verbose_name= u'Carro'
		verbose_name_plural=u'Carros'

class Busqueda(models.Model):
	idbusqueda = models.AutoField(primary_key=True,unique=True)
	Nombre=models.CharField(max_length=50)
	username=models.ForeignKey(User, on_delete=models.CASCADE)

	class Meta:
		verbose_name= u'busqueda'
		verbose_name_plural=u'busquedas'