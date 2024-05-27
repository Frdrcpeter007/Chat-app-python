from django.db.models import Count
from rest_framework import viewsets
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.response import Response

from .models import Server
from .schema import server_list_docs
from .serializer import ServerSerializer


class ServerListViewSet(viewsets.ViewSet):
    """
    Un viewset pour lister les serveurs avec divers filtres.

    Attributs:
        queryset (QuerySet): Le queryset initial de tous les objets Server.
    """
    queryset = Server.objects.all()

    @server_list_docs
    def list(self, request):
        """
        Liste les serveurs en fonction de divers paramètres de requête.

        Args:
            request (Request): L'objet de requête contenant les paramètres de requête.

        Paramètres de requête:
            category (str, optionnel): La catégorie pour filtrer les serveurs.
            limit (int, optionnel): Le nombre maximum de serveurs à retourner.
            by_user (str, optionnel): Si "true", filtre les serveurs par l'adhésion de l'utilisateur authentifié.
            server (int, optionnel): L'ID d'un serveur spécifique à récupérer.
            with_num_members (str, optionnel): Si "true", inclut le nombre de membres pour chaque serveur.

        Returns:
            Response: Un objet Response contenant les données des serveurs sérialisées.

        Raises:
            AuthenticationFailed: Si la requête n'est pas authentifiée et que 'by_user' ou 'server' est spécifié.
            ValidationError: Si 'server' est spécifié et que l'ID du serveur est invalide ou non trouvé.
        """
        # Récupération des paramètres de la requête
        category = request.query_params.get('category')
        limit = request.query_params.get('limit')
        by_user = request.query_params.get('by_user') == "true"
        server_id = request.query_params.get('server')
        with_num_members = request.query_params.get('with_num_members') == "true"

        # Vérification de l'authentification si 'by_user' ou 'server_id' est spécifié
        # if (by_user or server_id) and not request.user.is_authenticated:
        #     raise AuthenticationFailed(detail='Incorrect authentication credentials')

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
            if by_user and request.user.is_authenticated:
                user_id = request.user.id
                self.queryset = self.queryset.filter(member=user_id)
            else:
                raise AuthenticationFailed(detail='Incorrect authentication credentials')
        
        # Annoter le nombre de membres si 'with_num_members' est spécifié
        if with_num_members:
            self.queryset = self.queryset.annotate(num_members=Count("member"))

        # Limiter les résultats si 'limit' est spécifié
        if limit:
            self.queryset = self.queryset[:int(limit)]
        
        # Sérialiser la queryset avec les données du serveur
        serializer = ServerSerializer(self.queryset, many=True, context={"num_members": with_num_members})
        return Response(serializer.data)
