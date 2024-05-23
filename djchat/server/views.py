from django.db.models import Count
from rest_framework import viewsets
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.response import Response

from .models import Server
from .serializer import ServerSerializer


class ServerListViewSet(viewsets.ViewSet):
    # Définition de la queryset initiale qui récupère tous les objets Server
    queryset = Server.objects.all()

    def list(self, request):
        # Récupération des paramètres de la requête
        category = request.query_params.get('category')
        limit = request.query_params.get('limit')
        by_user = request.query_params.get('by_user') == "true"
        server_id = request.query_params.get('server')
        with_num_members = request.query_params.get('with_num_members') == "true"

        # Vérification de l'authentification si 'by_user' ou 'server_id' est spécifié
        if (by_user or server_id) and not request.user.is_authenticated:
            raise AuthenticationFailed(detail='Incorrect authentication credentials')

        # Filtrer par 'server_id' si spécifié
        if server_id:
            try:
                self.queryset = self.queryset.filter(id=server_id)

                # Vérification si le serveur existe
                if not self.queryset.exists():
                    raise ValidationError(detail=f'The server with id {server_id} not found')
            except ValueError:
                # Gestion des erreurs de conversion de 'server_id'
                raise ValidationError(detail='Something went wrong !')

        # Filtrer par 'category' si spécifié
        if category:
            self.queryset = self.queryset.filter(category=category)
        
        # Filtrer par utilisateur si 'by_user' est spécifié
        if by_user:
            user_id = request.user.id
            self.queryset = self.queryset.filter(member=user_id)
        
        # Annoter le nombre de membres si 'with_num_members' est spécifié
        if with_num_members:
            self.queryset = self.queryset.annotate(num_members=Count("member"))

        # Limiter les résultats si 'limit' est spécifié
        if limit:
            self.queryset = self.queryset[:int(limit)]
        
        # Sérialiser la queryset avec les données du serveur
        serializer = ServerSerializer(self.queryset, many=True, context={"num_members": with_num_members})
        return Response(serializer.data)
