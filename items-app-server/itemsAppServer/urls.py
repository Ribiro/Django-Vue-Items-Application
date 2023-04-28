from django.urls import path, include

urlpatterns = [
    path('api/', include('items_app.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
