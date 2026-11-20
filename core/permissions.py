import unicodedata

from rest_framework.permissions import IsAuthenticated


FULL_ACCESS_ROLES = {'administrador', 'dueno'}
OPERATIONAL_ROLES = {
    'mozo',
    'cadete',
    'ayudante de cocina',
    'planchero',
}


def normalize_role_name(name):
    normalized = unicodedata.normalize('NFKD', name or '')
    return ''.join(character for character in normalized if not unicodedata.combining(character)).strip().casefold()


def get_active_role_names(user):
    if not getattr(user, 'is_authenticated', False):
        return set()
    return {
        normalize_role_name(name)
        for name in user.usuarios_roles.filter(rol__estado=True).values_list('rol__nombre', flat=True)
    }


def is_full_access_user(user):
    return bool(
        getattr(user, 'is_superuser', False)
        or get_active_role_names(user).intersection(FULL_ACCESS_ROLES)
    )


def is_operational_user(user):
    roles = get_active_role_names(user)
    return not roles.intersection(FULL_ACCESS_ROLES) and bool(roles.intersection(OPERATIONAL_ROLES))


class RoleBasedIsAuthenticated(IsAuthenticated):
    message = 'No tiene permisos para acceder a este recurso.'

    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
        if is_full_access_user(request.user):
            return True
        if not is_operational_user(request.user):
            return False
        if not getattr(view, 'acceso_operativo_pedidos', False):
            return False
        if getattr(view, 'solo_listado_operativo', False):
            return request.method == 'GET' and getattr(view, 'action', None) == 'list'
        metodos_permitidos = getattr(view, 'metodos_operativos_permitidos', ())
        return request.method in metodos_permitidos
