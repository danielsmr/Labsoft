from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .forms import Login_Form, Registro, Nueva_Password, Agregar_producto, Consulta_nombre,Cantidad_consulta,Olvidar_Form
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.shortcuts import redirect
import json
from .models import User, Producto,Carro, Busqueda
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
import random 
from random import choice
from django.conf import settings
def Login(request):
	if request.user.is_authenticated:
		return redirect("/menu")
	else:
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
	if request.user.is_authenticated:
		print("menu")
	else:
		return redirect("/")

	return render (request, "menu.html", ctx)


def Regitrar_user(request):
	ctx={}
	if request.user.is_authenticated:
		return redirect("/menu")
	else:
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
	if request.user.is_authenticated:
		print("conf")
	else:
		return redirect("/")
	return render (request,"conf_cuenta.html" ,ctx)

def cambiar_contraseña(request):
	ctx={}
	if request.user.is_authenticated:
	
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
	else:
		return redirect("/")
	return render (request,"cambio_pass.html", ctx)



def agregar_productos(request):
	ctx={}
	if request.user.is_authenticated:
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
	else: 
		return redirect("/")
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
	
	if request.user.is_authenticated:
		register_form=Consulta_nombre(request.GET or None)
		suge=None
		objects = Producto.objects.all()
		msg=''
		if register_form.is_valid() and request.method == 'GET':
			
			form_data = register_form.cleaned_data
			title = form_data.get("Nombre")
			try:
				objects =Producto.objects.filter(Nombre=title)
				for elm in objects:
					tienda=elm.Tienda

				print (tienda)
				suge = Producto.objects.filter(Tienda=tienda)

				busqueda=Busqueda.objects.create(Nombre=title, username=request.user)
				
				print("guardo", title)
			except:
				msg="agrego"
		ctx = {
			"objects":objects,
			"suge":suge,
			"msg": msg,
			'register_form': register_form
		}
	else:
		return redirect("/")
	return render(request, "consulta.html", ctx)

def Anadir_lista(request,Codigo_barras):
	
	ctx={}
	if request.user.is_authenticated:
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
			try:	
				user = Carro.objects.last()
				if user.Vendido == True and user.username == request.user:
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
			except:

				print ("Creo")
				valor= random.randint(1, 99)
				print(valor)
				CodigoFactura="ABSD" + str(valor) 
				obje=Producto.objects.get(Codigo_barras=Codigo_barras)
				carro = Carro.objects.create(CodigoFactura=CodigoFactura, Codigo_barras=obje,username=request.user, Cantidad=cantidad, Vendido=False)
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
	else:
		return redirect('/')	
	
	return render (request,"Añadirprod.html",ctx)

def hacer_lista_nueva(request):
	
	obje=Carro.objects.all()
	
	for elem in obje:
		if elem.username == request.user and elem.Vendido==False:
			elem.Vendido=True
			elem.save()
			
	return redirect("/carro") 


def Carrito(request):
	ctx={}
	if request.user.is_authenticated:
		

		user = Carro.objects.filter(username=request.user, Vendido=False)
		total=0
		print(request.user)
		for elem in user:
			if elem.username==request.user:
				total=(elem.Cantidad * elem.Codigo_barras.Precio)+ total


		ctx={"user":user,
		"total": total, 
		}
	else:
		return redirect('/')
	
	
	return render (request,"carro.html",ctx)

def Historiales(request):
	ctx={}
	if request.user.is_authenticated:
		user = Busqueda.objects.filter(username=request.user)
		ctx={"user":user}
	else:
		return redirect('/')
	return render(request,"historial.html",ctx)



def Olvidar_Cuenta(request):
	if request.user.is_authenticated:
		return redirect('/menu')

	msg = ""
	olvidar_form = Olvidar_Form(request.POST or None)
	if olvidar_form.is_valid():
		form_data = olvidar_form.cleaned_data
		email = form_data.get('email')
		try: 
			user = User.objects.get(email=email)
		except User.DoesNotExist:
			user = None
		
		if user is not None:
			valores = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
			password = ""
			new_password = password.join([choice(valores) for i in range(8)])
			password = new_password
			new_password = make_password(password, salt=None, hasher='default')
			user.password = new_password
			user.save()
			send_password(1, user, password)
			msg = "Te hemos enviado un correo con tu nueva contraseña de ingreso. Revisa tu bandeja de entrada"
		else:
			msg = "No hay usuario con este email. Por favor registrate"

	ctx = {
		'olvidar_form' : olvidar_form,
		'msg' : msg
	}

	return render(request, "olvidar_cuenta.html", ctx)

def send_password(mode, user, password):
	if mode == 0:
		title = 'Registro en ePlayt'
		body = "Genial! Registro Completado\nBienvenido {}\nTu contraseña de ingreso es {}".format(user.username, password)
	else:
		title = "Recuperacion Contraseña en ePlayt"
		body = "Hola {}\nTu nueva contraseña de ingreso es {}".format(user.username,  password)

	send_mail(
		title,
		body,
	 	settings.EMAIL_HOST_USER,
		[user.email, 'elcrisol10smr@gmail.com'],
		fail_silently=False,
	)

def listar_user(request):
	ctx={}
	user=User.objects.all()
	ctx={
		"user": user
	}
	return render (request,"lista.html",ctx)
