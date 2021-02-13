
from rest_framework import serializers

from core.models import Tag, Ingredient ,Recipe


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag objects"""

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for ingredient objects"""
    # This is the ingredients serializer which is used for handling the ingredients
    # for our recipes in our recipe application

    class Meta:
        model = Ingredient
        fields = ('id', 'name')
        read_only_fields = ('id',)


class RecipeSerializer(serializers.Serializer):
    ingredients=serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Ingredient.objects.all()
    )
    tag=serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    class Meta:
        model=Recipe
        field=('id','title','ingredient','tags','time_minutes'
        ,'price','link')
        read_only_fields=('id')
