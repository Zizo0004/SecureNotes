from django.db import models
from django.contrib.auth.models import User


class Notes(models.Model):
    text = models.TextField()
    title = models.CharField(max_length=125)
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)


    def __str__ (self):
        return f"Note: {self.title}"