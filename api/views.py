from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.models import *
from .serializers import *
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings

from datetime import date
from django.db.models import Q

class EstadoAPIView(APIView):
    """
    Endpoint de ejemplo para confirmar que la API REST esta funcionando.

    Prueben visitarlo desde el navegador en:
        http://localhost:8000/api/estado/

    Sirve como punto de partida: reemplacen/amplien esta carpeta "api" con
    los serializers y vistas de los modelos reales de su organizacion
    (por ejemplo, ClienteSerializer, ClienteViewSet, etc.).
    """

    def get(self, request):
        return Response(
            {
                "estado": "ok",
                "mensaje": "La API REST del proyecto esta funcionando correctamente.",
            },
            status=status.HTTP_200_OK,
        )
   
class LoginAPIView(APIView):
    def post(self, request):
        user = get_object_or_404(Usuario, usuario=request.data['usuario'])
        if not user.check_password(request.data['password']):
            return Response({"error": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)
        
        token, created  = Token.objects.get_or_create(user=user)
        serializer = UsuarioSimplificadoSerializer(instance=user)
        
        return Response({"token": token.key, "user":serializer.data}, status=status.HTTP_200_OK)
    
class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            
            user = Usuario.objects.create_user(
                usuario=validated_data['usuario'],
                password=validated_data['password']
            )

            token = Token.objects.create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
         
class EmpleadosAPIView(APIView):
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        
        empleados = Empleado.objects.all().select_related(
            'local', 'usuario'
        ).prefetch_related(
            'usuario__usuarios_roles__rol'
        )
        
        serializer = EmpleadoSerializer(empleados, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        # Clonamos o limpiamos el request.data si 'local' viene como string vacío
        data = request.data.copy() if hasattr(request.data, 'copy') else request.data
        if data.get('local') == "":
            data['local'] = None

        serializer = EmpleadoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
class EmpleadosDetalleAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        empleado = get_object_or_404(Empleado, pk=pk)
        serializer = EmpleadoSerializer(empleado)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        empleado = get_object_or_404(Empleado, pk=pk)
        
        data = request.data.copy() if hasattr(request.data, 'copy') else request.data
        if data.get('local') == "":
            data['local'] = None

        # Pasamos la instancia existente para que ejecute el método 'update'
        serializer = EmpleadoSerializer(empleado, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
                
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        empleado = get_object_or_404(Empleado, pk=pk)
        
        empleado.delete()
        
        return Response("Empleado eliminado",status=status.HTTP_204_NO_CONTENT)
    
class PerfilAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # request.user te da el usuario autenticado gracias al Token
            # Buscas el empleado que esté asociado a ese usuario
            empleado = Empleado.objects.get(usuario=request.user)
            serializer = EmpleadoSerializer(empleado)
            return Response(serializer.data)
        
        except Empleado.DoesNotExist:
            return Response({"error": "No se encontró un empleado asociado a este usuario"}, status=404)

class LocalesAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        
        locales = Local.objects.all()
        
        serializer = LocalSerializer(locales, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class RolesAPIView(APIView):
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        
        roles = Rol.objects.all()
        
        serializer = RolSerializer(roles, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class InsumosAPIView(APIView):
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        
        insumos = Insumo.objects.all().select_related(
            'categoria'
        ).prefetch_related(
            'proveedores_insumos__proveedor'
        )
        
        serializer = InsumoSerializer(insumos, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = InsumoSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class InsumosDetalleAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        insumo = get_object_or_404(Insumo, pk=pk)
        serializer = InsumoSerializer(insumo)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        insumo = get_object_or_404(Insumo, pk=pk)

        serializer = InsumoSerializer(insumo, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response("Insumo actualizado", status=status.HTTP_200_OK)
                
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        insumo = get_object_or_404(Insumo, pk=pk)
        
        insumo.delete()
        
        return Response("Insumo eliminado", status=status.HTTP_200_OK)
 

class CategoriasAPIView(APIView):
        
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        
        categorias = Categoria.objects.all()
        
        serializer = CategoriaSerializer(categorias, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

class InsumosListadoAPIView(APIView):
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        
        insumos = Insumo.objects.all()
        
        serializer = InsumoSimplificadoSerializer(insumos, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProductosAPIView(APIView):
        
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        
        productos = Producto.objects.all().prefetch_related(
            'productos_insumos__insumo'
        )
        
        serializer = ProductoSerializer(productos, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = ProductoSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProductosDetalleAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        producto = get_object_or_404(Producto, pk=pk)
        serializer = ProductoSerializer(producto)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        producto = get_object_or_404(Producto, pk=pk)

        serializer = ProductoSerializer(producto, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response("Producto actualizado", status=status.HTTP_200_OK)
                
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        producto = get_object_or_404(Producto, pk=pk)
        
        producto.delete()
        
        return Response("Producto eliminado",status=status.HTTP_200_OK)
    
class ProductosListadoAPIView(APIView):
        
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        
        productos = Producto.objects.all()
        
        serializer = ProductoSimplificadoSerializer(productos, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ProveedoresAPIView(APIView):
        
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        
        proveedores = Proveedor.objects.all()
        
        serializer = ProveedorSerializer(proveedores, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

class MetodosDePagoAPIView(APIView):
        
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        
        metodos = MetodoPago.objects.all()
        
        serializer = MetodoPagoSerializer(metodos, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK) 

class DetallesVentaAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        
        detalles = DetalleVenta.objects.all().select_related(
            'producto'
        )
        
        serializer = DetalleVentaSerializer(detalles, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
   
class VentasAPIView(APIView):
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        
        ventas = Venta.objects.all().select_related(
            'metodo'
        ).prefetch_related(
            'detalles__producto'
        )
        
        
        serializer = VentaSerializer(ventas, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = VentaSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UsuariosAPIView(APIView):
        
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        
        usuarios = Usuario.objects.all()
        
        serializer = UsuarioSimplificadoSerializer(usuarios, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)


class ComprasAPIView(APIView):
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        
        compras = Compra.objects.all().prefetch_related(
            'detalles__insumo'
        )
        
        serializer = CompraSerializer(compras, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

class CajasAPIView(APIView):
        
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        
        cajas = Caja.objects.all().prefetch_related(
            'movimientos'
            )
        
        status_param = request.query_params.get('status', None)
        date_param = request.query_params.get('date', None)
        
        if status_param == 'active':
            cajas = cajas.filter(estado=True, fecha_hora_cierre__isnull=True)
            
        if date_param == 'today':
            hoy = date.today()
            
            # Filtramos si la caja abrió HOY o si cerró HOY
            # Q(...) | Q(...): Actúa como un operador OR en SQL. Esto asegura que si una caja se abrió ayer pero se cerró hoy, o viceversa, aparezca correctamente en el listado del día.
            
            cajas = cajas.filter(
                Q(fecha_hora_apertura__date=hoy) | Q(fecha_hora_cierre__date=hoy)
            )
        
        serializer = CajaSerializer(cajas, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = CajaSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class CajasDetalleAPIView(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        caja = get_object_or_404(Caja, pk=pk)
        serializer = CajaSerializer(caja)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, pk):
        caja = get_object_or_404(Caja, pk=pk)

        serializer = CajaSerializer(caja, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response("Caja actualizado", status=status.HTTP_200_OK)
                
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        

class PedidosAPIView(APIView):
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        
        pedidos = Pedido.objects.all().select_related(
            'empleado'
        ).prefetch_related(
            'detalles__producto'
        )
        
        date_param = request.query_params.get('date', None)
        
        if date_param == 'today':
            hoy = date.today()
            
            pedidos = pedidos.filter(fecha_hora_creacion__date=hoy)
        
        serializer = PedidoSerializer(pedidos, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = PedidoSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

class MenusAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        
        menus = Menu.objects.all().prefetch_related(
            'detalles'
        )
        
        serializer = MenuSerializer(menus, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)


















class PasswordResetRequestAPIView(APIView):
    """
    Paso 1: Recibe el email, genera el token y envía el correo con el enlace de recuperación.
    """
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({"error": "El email es obligatorio"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Buscamos en tu modelo Usuario personalizado
            user = Usuario.objects.get(email=email)
        except Usuario.DoesNotExist:
            # Por seguridad, se suele responder con éxito para no revelar qué emails existen en la BD
            return Response({"mensaje": "Si el correo existe, se han enviado las instrucciones."}, status=status.HTTP_200_OK)
        
        # Generar token y uid únicos
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        # Construir la URL del frontend a donde llegará el usuario
        reset_url = f"http://localhost:3000/#/authentication/change-password/{uid}/{token}/"
        
        subject = "Recuperación de contraseña"
        message = f"Hola {user.usuario},\n\nHas solicitado restablecer tu contraseña. Haz clic en el siguiente enlace:\n{reset_url}\n\nSi no lo solicitaste, ignora este mensaje."
        
        try:
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
        except Exception:
            return Response({"error": "Error al enviar el correo electrónico"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        return Response({"mensaje": "Correo de recuperación enviado exitosamente."}, status=status.HTTP_200_OK)

class PasswordResetConfirmAPIView(APIView):
    
    """
    Paso 2: Valida el UID y el Token de la URL, y actualiza la contraseña.
    """
    def post(self, request, uidb64, token):
        new_password = request.data.get('new_password')
        
        if not new_password:
            return Response({"error": "La nueva contraseña es obligatoria"}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            # Decodificar el ID del usuario
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = Usuario.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, Usuario.DoesNotExist):
            user = None
            
        # Verificar si el usuario existe y si el token es válido
        if user is not None and default_token_generator.check_token(user, token):
            user.set_password(new_password)
            user.save()
            return Response({"mensaje": "Contraseña actualizada exitosamente."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "El enlace de recuperación es inválido o ha expirado."}, status=status.HTTP_400_BAD_REQUEST)
        
        
        
        
