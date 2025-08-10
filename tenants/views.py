from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db import connection
from django_tenants.utils import schema_context
from .models import Center, Domain
from .serializers import CenterSerializer, DomainSerializer

class CenterViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Centers (tenants).
    Provides CRUD operations for centers.
    """
    queryset = Center.objects.all()
    serializer_class = CenterSerializer
    
    def create(self, request, *args, **kwargs):
        """
        Create a new center with its schema and domain.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Create center
        center = serializer.save()
        
        # Create domain for the center
        domain_name = f"{center.schema_name}.localhost"
        Domain.objects.create(
            domain=domain_name,
            tenant=center,
            is_primary=True
        )
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def migrate_schema(self, request, pk=None):
        """
        Run migrations for a specific tenant schema.
        """
        try:
            center = self.get_object()
            with schema_context(center.schema_name):
                from django.core.management import call_command
                call_command('migrate_schemas', schema_name=center.schema_name)
            
            return Response({'status': 'Schema migrated successfully'})
        except Exception as e:
            return Response(
                {'error': f'Migration failed: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False)
    def get_current_schema(self, request):
        """
        Get information about the current schema.
        """
        return Response({
            'schema_name': connection.schema_name,
            'tenant': getattr(connection.tenant, 'name', None) if hasattr(connection, 'tenant') else None
        })

class DomainViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Domains.
    """
    queryset = Domain.objects.all()
    serializer_class = DomainSerializer