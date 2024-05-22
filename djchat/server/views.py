from rest_framework import viewsets
from rest_framework.response import Response

from .models import Server
from .serializer import ServerSerializer


class ServerListViewSet(viewsets.ViewSet):

    queryset = Server.objects.all()

    def list(self, request):
        category = request.query_params.get('category')
        limit = request.query_params.get('limit')
        by_user = request.query_params.get('by_user') == "true"

        if category:
            self.queryset = self.queryset.filter(category=category)
        
        if by_user:
            print(request.user)
            user_id = request.user.id
            self.queryset = self.queryset.filter(member=user_id)

        if limit:
            self.queryset = self.queryset[:int(limit)]
        
        serializer = ServerSerializer(self.queryset, many=True) 
        return Response(serializer.data)