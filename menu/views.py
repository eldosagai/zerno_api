from rest_framework import viewsets, permissions
from menu.models import Category, Meal
from menu.serializers import CategorySerializer, MealSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]
    
    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAdminUser()]
        elif self.action in ['list']:
            return [permissions.AllowAny()]
        return super().get_permissions()

class MealViewSet(viewsets.ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAdminUser()]
        elif self.action in ['update', 'partial_update', 'list']:
            return [permissions.AllowAny()]
        return super().get_permissions()
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.AllowAny])
    def rate_meal(self, request, pk=None):
        meal = self.get_object()
        new_rating = request.data.get('rating')
        if new_rating is not None:
            meal.change_rating(float(new_rating))
            serializer = self.get_serializer(meal)
            return Response(serializer.data)
        else:
            return Response({"error": "Rating is required"}, status=status.HTTP_400_BAD_REQUEST)
        
    
    @action(methods=['post'], detail=False, permission_classes=[permissions.AllowAny])
    def get_meals(self, request, pk=None):
        ids = request.data.get('ids')
        if ids is not None:
            try:
                meals = Meal.objects.filter(id__in=ids)
                serialized_meals = MealSerializer(meals, many=True, context={'request': request}).data
                return Response(serialized_meals, status=200)
            except Meal.DoesNotExist:
                return Response({"error": "One or more meals not found."}, status=404)
        else:
            return Response({"error": "Please provide meal IDs."}, status=400)

            


