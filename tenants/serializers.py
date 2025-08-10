from rest_framework import serializers
from .models import Center, Domain

class CenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Center
        fields = ['id', 'name', 'description', 'schema_name', 'created_on', 'updated_on']
        read_only_fields = ['created_on', 'updated_on']
    
    def create(self, validated_data):
        # Auto-generate schema name from center name if not provided
        if 'schema_name' not in validated_data:
            schema_name = validated_data['name'].lower().replace(' ', '_').replace('-', '_')
            # Ensure schema name is unique
            counter = 1
            original_schema_name = schema_name
            while Center.objects.filter(schema_name=schema_name).exists():
                schema_name = f"{original_schema_name}_{counter}"
                counter += 1
            validated_data['schema_name'] = schema_name
        
        return super().create(validated_data)

class DomainSerializer(serializers.ModelSerializer):
    tenant_name = serializers.CharField(source='tenant.name', read_only=True)
    
    class Meta:
        model = Domain
        fields = ['id', 'domain', 'tenant', 'tenant_name', 'is_primary']