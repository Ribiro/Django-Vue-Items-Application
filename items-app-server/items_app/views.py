from .models import Item
from .serializers import ItemSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from django.db.models import Sum, Max, Min
from rest_framework.decorators import api_view
from rest_framework.decorators import action



# Create your views here.
class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Item.objects.filter(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        name = request.data["name"]
        price = request.data["price"]
        total_sales = request.data["total_sales"]
        description = request.data['description']
        image = request.data['image']
        
        user = request.user
        
        Item.objects.create(name=name, price=price, total_sales=total_sales, description=description, image=image, user=user)
        
        return Response("Item added successfully", status=status.HTTP_200_OK)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        user = request.user

        data = request.data.copy()  # create a mutable copy of the QueryDict
        data['user'] = user.id

        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        total_products = Item.objects.filter(user=request.user).count()
        total_sales = Item.objects.filter(user=request.user).aggregate(Sum('total_sales')).get('total_sales__sum')
        most_sold = Item.objects.filter(user=request.user).aggregate(Max('total_sales'))
        least_sold = Item.objects.filter(user=request.user).aggregate(Min('total_sales'))

        most_sold_product = Item.objects.filter(user=request.user, total_sales=most_sold['total_sales__max']).values_list('name', flat=True).first() or 'NA'
        least_sold_product = Item.objects.filter(user=request.user, total_sales=least_sold['total_sales__min']).values_list('name', flat=True).first() or 'NA'

        response_data = {
            'total_products': total_products,
            'total_sales': total_sales,
            'most_sold_product': most_sold_product,
            'least_sold_product': least_sold_product,
        }

        return Response(response_data, status=status.HTTP_200_OK)


