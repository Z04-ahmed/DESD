from django.db import models
from django.contrib.auth.hashers import make_password

class Student(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True, default="noemail@example.com")  # Default email for existing rows
    password = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        # Hash the password before saving (if not already hashed)
        if not self.pk or not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        super(Student, self).save(*args, **kwargs)

    def __str__(self):
        return self.username
