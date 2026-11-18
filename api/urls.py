from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    CategoriasAPIView,
    EmpleadosAPIView,
    EstadoAPIView,
    InsumosAPIView,
    LoginAPIView,
    MenuPermissionsAPIView,
    MenuViewSet,
    PasswordResetConfirmAPIView,
    PasswordResetRequestAPIView,
    ProductosAPIView,
    RegisterAPIView,
)

router = DefaultRouter()
router.register('menus', MenuViewSet, basename='menu')

urlpatterns = [
    path('estado/', EstadoAPIView.as_view(), name='api-estado'),
    path('empleados/', EmpleadosAPIView.as_view(), name='api-empleados'),
    path('insumos/', InsumosAPIView.as_view(), name='api-pnsumos'),
    path('productos/', ProductosAPIView.as_view(), name='api-productos'),
    path('login/', LoginAPIView.as_view(), name='api-login'),
    path('menus/permissions/', MenuPermissionsAPIView.as_view(), name='api-menu-permissions'),
    path('register/', RegisterAPIView.as_view(), name='api-register'),
    path('password-reset/', PasswordResetRequestAPIView.as_view(), name='api-password-reset'),
    path(
        'password-reset/confirm/',
        PasswordResetConfirmAPIView.as_view(),
        name='api-password-reset-confirm',
    ),
    path('categorias/', CategoriasAPIView.as_view(), name='api-categorias'),
    path('', include(router.urls)),
]
