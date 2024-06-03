from django.db import models
from django.contrib.auth.models import User
from SecureNotes.settings import CRYPTO_KEY
from cryptography.fernet import Fernet
from .views import decryption,encryption


class Notes(models.Model):
    text = models.TextField()
    title = models.CharField(max_length=125)
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.text = encryption(self.text,CRYPTO_KEY)
        super().save(*args,**kwargs)

    def __str__ (self):
        decrypyed_message = decryption(self.text,CRYPTO_KEY)
        return f"{self.title} : {decrypyed_message[1:25]}"