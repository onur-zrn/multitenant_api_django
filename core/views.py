from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import connection
from .models import Sample, SampleResult
from .serializers import SampleSerializer, SampleResultSerializer, SampleResultCreateSerializer

class SampleViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Samples in tenant schemas.
    """
    queryset = Sample.objects.all()
    serializer_class = SampleSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by status if provided
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by sample_type if provided
        type_filter = self.request.query_params.get('sample_type', None)
        if type_filter:
            queryset = queryset.filter(sample_type=type_filter)
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        
        if start_date:
            queryset = queryset.filter(collection_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(collection_date__lte=end_date)
        
        return queryset
    
    @action(detail=True, methods=['post'])
    def add_result(self, request, pk=None):
        """
        Add a test result to a sample.
        """
        sample = self.get_object()
        serializer = SampleResultCreateSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(sample=sample)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        """
        Update sample status.
        """
        sample = self.get_object()
        new_status = request.data.get('status')
        
        if new_status not in dict(Sample._meta.get_field('status').choices):
            return Response(
                {'error': 'Invalid status'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        sample.status = new_status
        sample.save()
        
        return Response({'status': 'Status updated successfully'})
    
    @action(detail=False)
    def statistics(self, request):
        """
        Get sample statistics for the current tenant.
        """
        total_samples = Sample.objects.count()
        status_counts = {}
        
        for status_choice, _ in Sample._meta.get_field('status').choices:
            status_counts[status_choice] = Sample.objects.filter(status=status_choice).count()
        
        return Response({
            'total_samples': total_samples,
            'status_distribution': status_counts,
            'current_schema': connection.schema_name
        })

class SampleResultViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Sample Results.
    """
    queryset = SampleResult.objects.all()
    serializer_class = SampleResultSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by sample if provided
        sample_id = self.request.query_params.get('sample', None)
        if sample_id:
            queryset = queryset.filter(sample_id=sample_id)
        
        # Filter by abnormal results
        is_abnormal = self.request.query_params.get('is_abnormal', None)
        if is_abnormal is not None:
            queryset = queryset.filter(is_abnormal=is_abnormal.lower() == 'true')
        
        return queryset