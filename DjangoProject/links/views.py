from rest_framework.views import APIView
from rest_framework.response import Response
from .models import AppLink
from .serializers import AppLinkSerializer

class AppLinkList(APIView):
    def get(self, request):
        apps = AppLink.objects.all()
        serializer = AppLinkSerializer(apps, many=True)
        return Response(serializer.data)
