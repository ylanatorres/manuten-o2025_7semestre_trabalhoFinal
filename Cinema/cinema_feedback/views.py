from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from managecinema.models import Cinema

from .models import Review
from .serializers import ReviewSerializer

class ReviewViewsets(generics.ListCreateAPIView):
    queryset = Review.objects.all().order_by('-created_at')
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=200)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.save()
            
            movie_id = request.data.get('movie')
            if movie_id:
                try:
                    cinema_query = Cinema.objects.get(id=movie_id)
                    cinema_query.all_review.add(data.id)
                except Cinema.DoesNotExist:
                    pass 
                    
        return Response(serializer.data, status=200)