from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
  title = models.CharField(max_length=200)
  description = models.TextField(max_length=10000)
  created = models.DateTimeField(auto_now_add=True)
  datecompleted = models.DateTimeField(null=True, blank=True)
  important = models.BooleanField(default=False)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  status = models.CharField(max_length=75, default='pendiente')
  imagen = models.ImageField(upload_to='productos/', blank=True, null=True)

  def __str__(self):
    return self.title + ' - ' + self.user.username