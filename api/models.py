from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Tasks(models.Model):
    task=models.CharField(max_length=100)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    description=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    due_date=models.DateField(blank=True,null=True)
    completed=models.BooleanField(default=False)
    completed_at=models.DateTimeField(auto_now_add=True,blank=True,null=True)

    def __str__(self):
        return self.task
    
