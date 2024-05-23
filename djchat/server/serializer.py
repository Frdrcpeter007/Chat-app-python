from django.conf import settings
from rest_framework import serializers

from .models import Category, Channel, Server


# Serializer pour le modèle Category
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category  # Modèle à sérialiser
        fields = ['id', 'name']  # Champs à inclure dans la sérialisation

# Serializer pour le modèle Channel
class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel  # Modèle à sérialiser
        fields = '__all__'  # Inclure tous les champs du modèle

# Serializer pour le modèle User (utilisateur)
class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = settings.AUTH_USER_MODEL  # Modèle utilisateur à partir des paramètres
        fields = ['id', 'username']  # Champs à inclure dans la sérialisation

# Serializer pour le modèle Server
class ServerSerializer(serializers.ModelSerializer):
    # Champ personnalisé pour le nombre de membres
    num_members = serializers.SerializerMethodField()
    # Sérialisation imbriquée pour la catégorie
    category = CategorySerializer(read_only=True)
    # Sérialisation imbriquée pour les channels (nombreux)
    channel_server = ChannelSerializer(read_only=True, many=True)

    class Meta:
        model = Server  # Modèle à sérialiser
        exclude = ("member",)  # Exclure le champ "member" de la sérialisation

    # Méthode pour obtenir le nombre de membres
    def get_num_members(self, obj):
        if hasattr(obj, 'num_members'):
            return obj.num_members
        return None

    # Personnalisation de la représentation des données
    def to_representation(self, instance):
        data = super().to_representation(instance)
        num_members = self.context.get('num_members')

        # Supprimer le champ 'num_members' si non nécessaire
        if not num_members:
            data.pop('num_members')
        
        return data
