from django.urls import path, re_path
from polls import views

urlpatterns = [
    path('', views.Login, name="index"),
    path('menu', views.menu, name="Menu"),
    path('registro', views.Regitrar_user,name='Registro'),
    path('configurar_cuenta', views.configuracion_cuenta,name='Configurar_Cuenta'),
    path('cambio_pass',views.cambiar_contraseña,name="Cambio_pass"),
    path('agregarproducto', views.agregar_productos, name="Agregar_producto"),
    path('adios', views.Sign_out, name="Adios"),
    path('consulta', views.Consulta, name="Consulta"),
    path('carro', views.Carrito, name="Carro"),
    path('historial', views.Historiales, name="Historial"),
    path('anadir/<Codigo_barras>',views.Anadir_lista,name="Anadir"),
    path('hacernuevalista', views.hacer_lista_nueva,name="HacerNuevaLista"),
    path('olvidar_cuenta/', views.Olvidar_Cuenta, name='olvidar_cuenta'),
    path('listar_user', views.listar_user, name="Listar_user")
]
