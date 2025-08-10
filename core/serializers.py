from rest_framework import serializers
from .models import Sample, SampleResult

class SampleResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleResult
        fields = [
            'id', 'test_name', 'result_value', 'unit', 
            'reference_range', 'is_abnormal', 'notes', 'created_at'
        ]

class SampleSerializer(serializers.ModelSerializer):
    results = SampleResultSerializer(many=True, read_only=True)
    results_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Sample
        fields = [
            'id', 'name', 'description', 'sample_type', 'collection_date',
            'processed_date', 'status', 'metadata', 'created_by',
            'results', 'results_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'created_by']
    
    def get_results_count(self, obj):
        return obj.results.count()
    
    def create(self, validated_data):
        # Set created_by from request user
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['created_by'] = request.user.email
        return super().create(validated_data)

class SampleResultCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleResult
        fields = [
            'sample', 'test_name', 'result_value', 'unit',
            'reference_range', 'is_abnormal', 'notes'
        ]
