from django.db import models
from users.models import UserAccount

# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    image = models.ImageField(upload_to= 'img', blank=True, null=True)
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)