from rest_framework import serializers
from menu.models import Category, Meal


class MealSerializer(serializers.HyperlinkedModelSerializer):
    categoryName = serializers.SerializerMethodField()
    
    class Meta:
        model = Meal
        fields = ['url', 'id', 'name', 'price', 'rating',
                  'description', 'image','categoryName','category']

    def get_categoryName(self, obj):
        return obj.category.name


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    meals = MealSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['url', 'id', 'name', 'meals']