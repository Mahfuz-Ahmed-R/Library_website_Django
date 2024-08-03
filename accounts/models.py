from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserAccountModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
