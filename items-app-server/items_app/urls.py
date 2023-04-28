from django.urls import path, include

from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('item', views.ItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('item/stats/', views.ItemViewSet.as_view({'get': 'stats'}), name='item-stats'),
]