from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Todo(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    todo_nombre = models.CharField(max_length=1000)
    estado = models.BooleanField(default=False)


    def __str__(self):
        
        return self.todo_nombre

