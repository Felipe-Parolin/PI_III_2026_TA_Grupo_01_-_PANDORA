from rest_framework.permissions import IsAuthenticated


class EmpresaQuerysetMixin:
    permission_classes = [IsAuthenticated]

    def get_empresa(self):
        return getattr(self.request.user, 'empresa', None)

    def is_superuser(self):
        return getattr(self.request.user, 'is_superuser', False)

    def filter_by_empresa(self, queryset, empresa_field='empresa'):
        if self.is_superuser():
            return queryset
        empresa = self.get_empresa()
        if not empresa:
            return queryset.none()
        return queryset.filter(**{empresa_field: empresa})
