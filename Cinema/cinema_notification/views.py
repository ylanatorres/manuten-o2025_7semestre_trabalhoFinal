from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Notification
from .serializers import NotificationSerializer

class NotificationListView(generics.ListAPIView):
    queryset = Notification.objects.all().order_by('-created_at')
    serializer_class = NotificationSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        Notification.notification_read(self=self, user=self.request.user)
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=200)

class UnreadNotificationCount(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        count = Notification.objects.filter(user=request.user, read=False).count()
        return Response({'count': count}, status=200)