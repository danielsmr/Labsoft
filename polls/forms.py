from django import forms
from .models import User,Producto,Carro

class Login_Form(forms.Form):
	username = forms.CharField(max_length=50)
	password = forms.CharField(max_length=50)

class Registro(forms.ModelForm):
	class Meta:
		model = User
		fields=['username', 'password', 'email', 'fecha_nacimiento']


class Nueva_Password(forms.Form):
	password_actual = forms.CharField(max_length=50)
	password_nueva = forms.CharField(max_length=50)
	password_confirmar = forms.CharField(max_length=50)

class Agregar_producto(forms.ModelForm):
	class Meta:
		model = Producto
		fields=['Codigo_barras','Nombre', 'Tienda', 'Precio','Descripcion']

class Consulta_nombre(forms.ModelForm):
	Nombre = forms.CharField(max_length=200)
	class Meta:
		model = Producto
		fields=['Nombre']

class Cantidad_consulta(forms.ModelForm):
	class Meta:
		model=Carro
		fields=['Cantidad']