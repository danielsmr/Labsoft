from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .forms import Login_Form, Registro, Nueva_Password, Agregar_producto, Consulta_nombre,Cantidad_consulta
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.shortcuts import redirect
import json
from .models import User, Producto,Carro
from django.contrib.auth.hashers import make_password

import random 


def Login(request):
	login_form = Login_Form(request.POST or None)
	msg = ''
	if login_form.is_valid():
		form_data = login_form.cleaned_data
		username = form_data.get('username')
		password = form_data.get('password')
		print (username)
		try:
			user = User.objects.get(username=username)
		except User.DoesNotExist:
			user = None
		if user is not None:
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				return redirect("/menu")
			else:
				msg = 'Contraseña incorrecta'
		else: 
			msg = 'No existe Usuario'

	ctx = {
		'login_form' : login_form,
		'msg' : msg,
	}

	return render(request, "index.html", ctx)

def menu(request):
	ctx={}
	return render (request, "menu.html", ctx)


def Regitrar_user(request):
	ctx={}
	register_form = Registro(request.POST or None)

	if register_form.is_valid():
		form_data = register_form.cleaned_data
		user = form_data.get('username')
		try: 
			user = User.objects.get(username=user)
		except User.DoesNotExist:
			user = None
		
		if user is None:
			username = form_data.get("username")
			print(username)
			email = form_data.get("email")
			print(email)
			pword = form_data.get("password")
			print(pword)
			password = make_password(pword, salt=None, hasher='default')
			print(password)
			fecha_nacimiento = form_data.get("fecha_nacimiento")
			print(fecha_nacimiento)
			user = User.objects.create(username=username, password=password, email=email, fecha_nacimiento=fecha_nacimiento, is_active=True)
			print("guardado")
			return redirect("/")

	ctx = {'register_form': register_form}
	return render(request, "registro.html", ctx)

def Sign_out(request):
	logout(request)
	return redirect("/")

def configuracion_cuenta(request):
	ctx={}
	return render (request,"conf_cuenta.html" ,ctx)

def cambiar_contraseña(request):
	ctx={}
	nueva_password = Nueva_Password(request.POST or None)
	msg_password=''
	if nueva_password.is_valid():

		form_data = nueva_password.cleaned_data
		password_actual = form_data.get("password_actual")
		password_nueva = form_data.get("password_nueva")
		password_confirmar = form_data.get("password_confirmar")
		print (password_nueva)
		acceso = authenticate(username=request.user.username, password=password_actual)
		if acceso is not None:
			if password_nueva == password_confirmar:
				request.user.password = make_password(password_nueva, salt=None, hasher='default')	
				request.user.save()
				print("cambio")
				msg_password = 'Contraseña actualizada satisfactoriamente'
			else:
				msg_password = 'Las contraseñas nueva y la confirmacion no coinciden'
		else:
			msg_password = 'Contraseña incorrecta'

	ctx={
		'nueva_password' : nueva_password,
		'msg_password' : msg_password
	}
	return render (request,"cambio_pass.html", ctx)



def agregar_productos(request):
	ctx={}
	register_form = Agregar_producto(request.POST or None)
	msg=''
	if register_form.is_valid():
		form_data = register_form.cleaned_data
		user = form_data.get('Codigo_barras')
		try: 
			user = Producto.objects.get(Codigo_barras=user)
		except Producto.DoesNotExist:
			user = None
		
		if user is None:
			Codigo_barras = form_data.get("Codigo_barras")
			print(Codigo_barras)
			Nombre = form_data.get("Nombre")
			print(Nombre)
			Tienda = form_data.get("Tienda")
			print(Tienda)
			Precio = form_data.get("Precio")
			print(Precio)
			Descripcion = form_data.get("Descripcion")
			print(Descripcion)
			prodcuto = Producto.objects.create(Codigo_barras=Codigo_barras, Nombre=Nombre, Tienda=Tienda, Precio=Precio, Descripcion=Descripcion)
			print("guardado")
			msg='Producto guardado'
		else:
			msg='Codigo ya registrado'

	ctx = {'register_form': register_form,
			'msg': msg}
	return render(request,"AgregarProducto.html", ctx)


'''
def regis_articulos(request, idProducto):

	Artic = articulo.objects.all()

	if len(Artic) == 0:
		prod= Producto.objects.get(idProducto = idProducto)
		
		articuloc = articulo.objects.create(idProducto = prod, Cantidad = "1")
	else:
		articuloc= articulo.objects.get(idProducto = idProducto)
		articuloc.Cantidad=str(int(articuloc.Cantidad)+1)
		articuloc.save()

	return redirect("/registro_v/" + str(articuloc.idarticulo))

'''
def Consulta(request):
	register_form=Consulta_nombre(request.GET or None)
	
	objects = Producto.objects.all()

	if register_form.is_valid() and request.method == 'GET':
		
		form_data = register_form.cleaned_data
		title = form_data.get("Nombre")
		objects =Producto.objects.filter(Nombre=title)
		print (title)
	

			
	ctx = {
		"objects":objects,
		
		'register_form': register_form
	}
	return render(request, "consulta.html", ctx)

def Anadir_lista(request,Codigo_barras):
	ctx={}
	
	print(Codigo_barras)

	objects =Producto.objects.filter(Codigo_barras=Codigo_barras)

	for elem in objects:
		objects_Codigo=elem.Codigo_barras
		objects_Nombre=elem.Nombre
		objects_Tienda=elem.Tienda
		objects_Precio=elem.Precio
		objects_des=elem.Descripcion

	register_form=Cantidad_consulta(request.POST or None)

	if register_form.is_valid() and request.method == 'POST':
		vendido=True
		form_data = register_form.cleaned_data
		cantidad = form_data.get("Cantidad")
		print("cantidad", cantidad)
				
		user = Carro.objects.last()
		if user.Vendido == True:
			user=None	
			print (user)

		if user is  None:
			print ("Creo")
			valor= random.randint(1, 99)
			print(valor)
			CodigoFactura="ABSD" + str(valor) 
			obje=Producto.objects.get(Codigo_barras=Codigo_barras)
			carro = Carro.objects.create(CodigoFactura=CodigoFactura, Codigo_barras=obje,username=request.user, Cantidad=cantidad, Vendido=False)
			return redirect("/consulta")
		else:
			
			objects=Carro.objects.last()
			obje=Producto.objects.get(Codigo_barras=Codigo_barras)
			carro = Carro.objects.create(CodigoFactura=objects.CodigoFactura, Codigo_barras=obje,username=request.user, Cantidad=cantidad, Vendido=False)
			print ("agrego")
			return redirect("/consulta")


	


	ctx = {
		"objects":objects,
		"objects_Codigo":objects_Codigo,
		"objects_Nombre":objects_Nombre,
		"objects_Tienda":objects_Tienda,
		"objects_Precio":objects_Precio,
		"objects_des":objects_des,
		'register_form':register_form
	}
	
	return render (request,"Añadirprod.html",ctx)


def Carrito(request):
	ctx={}
	user = Carro.objects.filter(username=request.user, Vendido=False)
	total=0
	for elem in user:
		total=(elem.Cantidad * elem.Codigo_barras.Precio)+ total

	ctx={"user":user,
		"total": total}


def Historiales(request):
	ctx={}
	user = Carro.objects.filter(username=request.user, Vendido=True)
	return render(request,"historial.html",ctx)
