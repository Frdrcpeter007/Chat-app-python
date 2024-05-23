from django.conf import settings
from rest_framework import serializers

from .models import Category, Channel, Server


class CategorySerializer(serializers.ModelSerializer):
    """Sérialiseur pour le modèle Category.

    Ce sérialiseur gère la conversion des instances du modèle Category
    vers et depuis le format JSON.

    Attributs:
        Meta: Classe de configuration pour le sérialiseur.
    """

    class Meta:
        model = Category
        fields = ['id', 'name']

class ChannelSerializer(serializers.ModelSerializer):
    """Sérialiseur pour le modèle Channel.

    Ce sérialiseur gère la conversion des instances du modèle Channel
    vers et depuis le format JSON.

    Attributs:
        Meta: Classe de configuration pour le sérialiseur.
    """

    class Meta:
        model = Channel
        fields = '__all__'

class OwnerSerializer(serializers.ModelSerializer):
    """Sérialiseur pour le modèle Utilisateur.

    Ce sérialiseur gère la conversion des instances du modèle Utilisateur
    vers et depuis le format JSON.

    Attributs:
        Meta: Classe de configuration pour le sérialiseur.
    """

    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = ['id', 'username']

class ServerSerializer(serializers.ModelSerializer):
    """Sérialiseur pour le modèle Server.

    Ce sérialiseur gère la conversion des instances du modèle Server
    vers et depuis le format JSON. Il inclut des sérialiseurs imbriqués
    pour les modèles Category et Channel, ainsi qu'un champ personnalisé
    pour le nombre de membres.

    Attributs:
        num_members (SerializerMethodField): Champ personnalisé pour compter le nombre de membres.
        category (CategorySerializer): Sérialiseur imbriqué pour la catégorie.
        channel_server (ChannelSerializer): Sérialiseur imbriqué pour les channels.
    """

    num_members = serializers.SerializerMethodField()
    category = CategorySerializer(read_only=True)
    channel_server = ChannelSerializer(read_only=True, many=True)

    class Meta:
        model = Server
        exclude = ("member",)

    def get_num_members(self, obj):
        """Obtient le nombre de membres pour un serveur.

        Args:
            obj (Server): L'instance du serveur.

        Returns:
            int ou None: Le nombre de membres s'il est disponible, sinon None.
        """
        if hasattr(obj, 'num_members'):
            return obj.num_members
        return None

    def to_representation(self, instance):
        """Personnalise la représentation de l'instance du serveur.

        Cette méthode personnalise la représentation JSON de l'instance
        du serveur en excluant éventuellement le champ `num_members` en
        fonction du contexte.

        Args:
            instance (Server): L'instance du serveur à représenter.

        Returns:
            dict: La représentation personnalisée de l'instance du serveur.
        """
        data = super().to_representation(instance)
        num_members = self.context.get('num_members')

        if not num_members:
            data.pop('num_members')
        
        return data
